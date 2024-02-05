#!/usr/bin/env python3

import re

def new_grid():
    g = []
    for i in range(1000):
        g.append([0]*1000)
    return g

def apply1(g, action):
    tl, br = re.findall(r'(\d+),(\d+)', action)
    top, left = int(tl[0]), int(tl[1])
    bottom, right = int(br[0]), int(br[1])
    for row in range(top, bottom+1):
        for col in range(left, right+1):
            if action.startswith('turn on'):
                g[row][col] += 1
            elif action.startswith('turn off'):
                g[row][col] -= 1
                if g[row][col] < 0:
                    g[row][col] = 0
            else:
                g[row][col] += 2
    return g

def count(g):
    return sum(sum(row) for row in g)

def run(inp):
    g = new_grid()
    for action in inp.strip().splitlines():
        g = apply1(g, action)
    return count(g)

example_input = """
turn on 0,0 through 0,0
toggle 0,0 through 999,999
"""

assert run(example_input) == 2000001

real_input = open('inputs/day06.input.txt').read()
print(run(real_input)) # => 15343601
