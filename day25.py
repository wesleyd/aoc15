#!/usr/bin/env python3

import re

def nth(i, n=20151125):
    while i-1:
        n = (n * 252533) % 33554393
        i -= 1
    return n

def i_at(row, col):
    i = 1
    for r in range(row):
        i += r
    for c in range(col-1):
        i += row+(c+1)
    return i
assert i_at(4,2) == 12
assert i_at(2,4) == 14
assert i_at(4,3) == 18
assert i_at(6,1) == 16
assert i_at(1,6) == 21

def n_at(row, col):
    return nth(i_at(row, col))
assert n_at(1,1) == 20151125
assert n_at(6,1) == 33071741
assert n_at(1,6) == 33511524
assert n_at(6,6) == 27995004

real_input = open('inputs/day25.input.txt').read()
def parse(inp):
    return [int(x) for x in re.findall(r'\d+', inp)]
row, col = parse(real_input)
print(n_at(row, col))  # => 8997277
