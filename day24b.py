#!/usr/bin/env python3

import itertools
import math
import operator

from functools import reduce
from typing import Iterator, List, Set

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

def balance(pkgs: Set[int], n: int) -> Iterator[List[Set[int]]]:
    """All ways to extract n equal-weight groups from pkgs."""
    if n == 1:
        yield [pkgs]
        return
    target_weight = sum(pkgs) // n
    max_pkgs = len(pkgs) // n
    for i in range(1, max_pkgs+1):
        for group in itertools.combinations(pkgs, i):
            if sum(group) != target_weight:
                continue
            g = set(group)
            if can_balance(pkgs - g, n-1):
                yield g
def can_balance(pkgs: Set[int], n: int) -> bool:
    for _ in balance(pkgs, n):
        return True
    return False
assert list(balance(example_packages, 4)) == [{11, 4}, {10, 5}, {8, 7}]

def run(pkgs):
    smallest_qe = math.inf
    shortest = math.inf
    for passenger in balance(pkgs, 4):
        if len(passenger) > shortest:
            break
        if len(passenger) < shortest:
            shortest = len(passenger)
        qe = reduce(operator.mul, passenger)
        if qe < smallest_qe:
            smallest_qe = qe
    return smallest_qe

real_input = open('inputs/day24.input.txt').read()
real_packages = parse(real_input)
print(run(real_packages))
