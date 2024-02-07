#!/usr/bin/env python3

import math

from collections import defaultdict

example_input = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

def parse(inp):
    distances = defaultdict(dict)
    for line in inp.strip().splitlines():
        l, r = line.split(" = ")
        a, z = l.split(" to ")
        distances[a.strip()][z.strip()] = int(r)
        distances[z.strip()][a.strip()] = int(r)
    return distances

example_distances = parse(example_input)

def peek(d, n=0):
    """Return the nth element in d. Dicts are ordered now."""
    if n < 0:
        n = -1-n
        d = reversed(d)
    for x in d:
        if n == 0:
            return x
        n -= 1

def walk(distances, path=None):
    if path is None:
        path = {}
        for nxt in distances.keys():
            yield from walk(distances, {nxt: 0})
    else:
        at = peek(path, -1)
        walked = False
        for nxt in distances[at].keys():
            if nxt not in path:
                path2 = dict(path)
                path2[nxt] = distances[at][nxt]
                yield from walk(distances, path2)
                walked = True
        if not walked:
            yield path

def longest(distances):
    s = -math.inf
    for path in walk(distances):
        d = sum(path.values())
        if d > s:
            s = d
    return s

assert longest(example_distances) == 982

real_input = open('inputs/day09.input.txt').read()
real_distances = parse(real_input)
print(longest(real_distances)) # => 909
