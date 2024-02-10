#!/usr/bin/env python3

import math
import re

from collections import namedtuple

example_input = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

Reindeer = namedtuple('Reindeer', ['v', 't', 'r'])

def parse(inp):
    d = {}
    for line in inp.strip().splitlines():
        pat = r'([A-Za-z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.'
        m = re.match(pat, line)
        assert m, line
        d[m[1]] = Reindeer(v=int(m[2]), t=int(m[3]), r=int(m[4]))
    return d
example_reindeers = parse(example_input)

def run1(r: Reindeer, t: int) -> int:
    n = t // (r.t + r.r)
    dist = n * r.v * r.t
    m = t % (r.t + r.r)
    dist += min(m, r.t) * r.v
    return dist

assert run1(example_reindeers['Comet'], 1) == 14
assert run1(example_reindeers['Dancer'], 1) == 16
assert run1(example_reindeers['Comet'], 10) == 140
assert run1(example_reindeers['Dancer'], 10) == 160
assert run1(example_reindeers['Comet'], 11) == 140
assert run1(example_reindeers['Dancer'], 11) == 176
assert run1(example_reindeers['Comet'], 12) == 140
assert run1(example_reindeers['Dancer'], 12) == 176
assert run1(example_reindeers['Comet'], 1000) == 1120
assert run1(example_reindeers['Dancer'], 1000) == 1056

def run(reindeers, t):
    furthest = -math.inf
    for r in reindeers.values():
        dist = run1(r, t)
        if dist > furthest:
            furthest = dist
    return furthest
assert run(example_reindeers, 1000) == 1120

real_input = open('inputs/day14.input.txt').read()
real_reindeers = parse(real_input)

print(run(real_reindeers, 2503)) # => 2640
