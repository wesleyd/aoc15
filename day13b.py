#!/usr/bin/env python3

import math
import re

from itertools import permutations

example_input = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

def parse(inp):
    grudges = {}
    for line in inp.strip().splitlines():
        m = re.fullmatch(r"([A-Za-z]+) would (gain|lose) (\d+) happiness units by sitting next to ([A-Za-z]+).", line)
        x = int(m.group(3))
        if m.group(2) == "lose":
            x = -x
        grudges[(m.group(1), m.group(4))] = x
    return grudges
example_grudges = parse(example_input)

def people(grudges):
    p = set()
    for a, b in grudges:
        p.add(a)
        p.add(b)
    p.add('me')
    return list(p)

def score(grudges, p):
    n = 0
    for j in range(len(p)):
        i, k = j-1, j+1
        if j == 0:
            i = len(p)-1
        if j == len(p)-1:
            k = 0
        n += grudges.get((p[j], p[i]), 0) + grudges.get((p[j], p[k]), 0)
    return n
assert score(example_grudges, ['Alice', 'Bob', 'Carol', 'David']) == 330

def arrange(inp):
    grudges = parse(inp)
    them = people(grudges)
    happiest = -math.inf
    for p in permutations(them):
        h = score(grudges, p)
        if h > happiest:
            happiest = h
    return happiest

real_input = open('inputs/day13.input.txt').read()
print(arrange(real_input)) # => 725
