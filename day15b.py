#!/usr/bin/env python3

import re

from collections import defaultdict
from typing import Dict

example_input = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""

def parse(inp):
    ingredients = defaultdict(dict)
    for line in inp.strip().splitlines():
        ingredient, rest = line.split(':')
        for piece in rest.split(','):
            m = re.search(r'([a-z]+) (-?\d+)', piece)
            p, q = m.group(1), int(m.group(2))
            ingredients[ingredient][p] = q
    return ingredients
example_ingredients = parse(example_input)

def bake1(ingredients, tsps: Dict[str, int]) -> int:
    assert len(ingredients) == len(tsps), (ingredients, tsps)
    pq = defaultdict(int)
    for ingredient, ntsps in tsps.items():
        for p, q in ingredients[ingredient].items():
            pq[p] += ntsps * q
    score = 1
    calories = 0
    for p, q in pq.items():
        if p == 'calories':
            calories = q
            continue
        if q < 0:
            return 0
        score *= q
    if calories == 500:
        return score
    return 0
assert bake1(example_ingredients, {'Butterscotch': 40, 'Cinnamon': 60}) == 57600000

def peek(d):
    for k in d:
        return k

def bake(ingredients, tsps=None):
    if not tsps:
        tsps = {}
    if len(tsps) == len(ingredients):
        yield bake1(ingredients, tsps)
    elif len(tsps) == len(ingredients) - 1:
        q = 100 - sum(tsps.values())
        assert q >= 0, tsps
        tsps2 = dict(tsps)
        ing = peek(ingredients.keys() - tsps.keys())
        tsps2[ing] = q
        yield from bake(ingredients, tsps2)
    else:
        n = sum(tsps.values())
        for i in range(100 - n):
            tsps2 = dict(tsps)
            ing = peek(ingredients.keys() - tsps.keys())
            tsps2[ing] = i
            yield from bake(ingredients, tsps2)

def run(ingredients):
    return max(bake(ingredients))
assert run(example_ingredients) == 57600000

real_input = open('inputs/day15.input.txt').read()
real_ingredients = parse(real_input)
print(run(real_ingredients))  # => 11171160
