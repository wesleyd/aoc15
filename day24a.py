#!/usr/bin/env python3

import itertools
import math
import operator

from functools import reduce
from typing import Iterator, Set

example_input = """
1
2
3
4
5
7
8
9
10
11
"""

def parse(inp):
    return {int(line) for line in inp.strip().splitlines()}
example_packages = parse(example_input)

def balance(pkgs: Set[int], ngroups: int) -> Iterator[Set[int]]:
    """All ways to extract equal weight 1/ngroups-th from pkgs, fewest first."""
    target_weight = sum(pkgs) // ngroups
    max_pkgs = len(pkgs) // ngroups
    for n in range(1, max_pkgs+1):
        for group in itertools.combinations(pkgs, n):
            if sum(group) != target_weight:
                continue
            yield set(group)

def can_split_in_half(pkgs: Set[int]) -> bool:
    """True if pkgs *can* be split into two equal-weight groups."""
    for group in balance(pkgs, 2):
        return group
    return False
assert not can_split_in_half({19,2,3,6})

def all_smallest3(pkgs: Set[int]) -> Iterator[Set[int]]:
    """All the combinations of the smallest third by weight of packages."""
    smallest = math.inf
    for group in balance(pkgs, 3):
        if len(group) < smallest:
            smallest = len(group)
        if len(group) > smallest:
            return
        yield group
assert list(all_smallest3(example_packages)) == [{9,11}]

def balance3(pkgs: Set[int]):
    smallest_qe = math.inf
    for passenger in all_smallest3(pkgs):
        if not can_split_in_half(pkgs - passenger):
            continue
        qe = reduce(operator.mul, passenger)
        if qe < smallest_qe:
            smallest_qe = qe
    return smallest_qe
assert balance3(example_packages) == 99

real_input = open('inputs/day24.input.txt').read()
real_packages = parse(real_input)
balance3(real_packages) # => 10439961859
