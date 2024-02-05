#!/usr/bin/env python3

import re

example_input = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

def new_circuit():
    return {}

def lookup(c, arg):
    if re.fullmatch(r'\d+', arg):
        return int(arg)
    else:
        return c[arg]

def apply1(c, action):
    lhs, target = re.search(r'(.*) -> ([a-z]+)', action).groups()
    lhs = lhs.split()
    match lhs:
        case (l, 'AND', r):
            c[target] = lookup(c, l) & lookup(c, r)
        case (l, 'OR', r):
            c[target] = lookup(c, l) | lookup(c, r)
        case (l, 'LSHIFT', r):
            c[target] = lookup(c, l) << lookup(c, r)
        case (l, 'RSHIFT', r):
            c[target] = lookup(c, l) >> lookup(c, r)
        case ('NOT', r):
            c[target] = ~ lookup(c, r)
            if c[target] < 0:
                c[target] &= 0xffff
        case [r]:
            c[target] = lookup(c, r)

def run(inp):
    c = new_circuit()
    actions = inp.strip().splitlines()
    while actions:
        action = actions.pop(0)
        try:
            apply1(c, action)
        except KeyError:  # LOL
            actions.append(action)
    return c

want = {
    'd': 72,
    'e': 507,
    'f': 492,
    'g': 114,
    'h': 65412,
    'i': 65079,
    'x': 123,
    'y': 456,
}
assert run(example_input) == want

real_input = open('inputs/day07.input.txt').read()
print(run(real_input)['a']) # => 3176
