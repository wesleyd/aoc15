#!/usr/bin/env python3

from collections import defaultdict
from itertools import chain

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
    return gifts

def multisanta(directions):
    gifts1 = santa(directions[::2])
    gifts2 = santa(directions[1::2])
    gifts = defaultdict(int)
    for house, ngifts in chain(gifts1.items(), gifts2.items()):
        gifts[house] += ngifts
    return sum(1 if v else 0 for v in gifts.values())
assert multisanta('^v') == 3
assert multisanta('^>v<') == 3
assert multisanta('^v^v^v^v^v') == 11

print(multisanta(open('inputs/day03.input.txt').read()))
