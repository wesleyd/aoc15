#!/usr/bin/env python3

from collections import defaultdict

def santa(directions):
    gifts = defaultdict(int)
    x, y = 0, 0
    gifts[(x,y)] = 1
    for direction in directions.strip():
        if direction == '^':
            y += 1
        elif direction == 'v':
            y -= 1
        elif direction == '<':
            x -= 1
        elif direction == '>':
            x += 1
        gifts[(x,y)] += 1
    return sum(1 if v else 0 for v in gifts.values())
assert santa('>') == 2
assert santa('^>v<') == 4
assert santa('^v^v^v^v^v') == 2

santa(open('inputs/day03.input.txt').read())
