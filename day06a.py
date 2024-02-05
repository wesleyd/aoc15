#!/usr/bin/env python3

import re

def new_grid():
    g = []
    for i in range(1000):
        g.append([False]*1000)
    return g

def apply1(g, action):
    tl, br = re.findall(r'(\d+),(\d+)', action)
    top, left = int(tl[0]), int(tl[1])
    bottom, right = int(br[0]), int(br[1])
    for row in range(top, bottom+1):
        for col in range(left, right+1):
            if action.startswith('turn on'):
                g[row][col] = True
            elif action.startswith('turn off'):
                g[row][col] = False
            else:
                g[row][col] = not g[row][col]
    return g

def count(g):
    n = 0
    for row in g:
        n += sum(1 if b else 0 for b in row)
    return n

g = new_grid()
assert count(g) == 0
g = apply1(g, 'turn on 0,0 through 999,999')
assert count(g) == 1_000_000
g = apply1(g, 'toggle 0,0 through 999,0')
assert count(g) == 999_000
g = apply1(g, 'turn off 499,499 through 500,500')
assert count(g) == 998_996

def run(actions):
    g = new_grid()
    for action in actions.splitlines():
        g = apply1(g, action)
    return count(g)

real_input = open('inputs/day06.input.txt').read().strip()
print(run(real_input)) # => 400410
