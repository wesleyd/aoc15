#!/usr/bin/env python3

import re

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

def replace_b(actions, n):
    for i in range(len(actions)):
        if re.fullmatch(r'(\d+) -> b', actions[i]):
            actions[i] = f'{n} -> b'
            return

def applyall(c, actions):
    actions = actions[:]
    while actions:
        action = actions.pop(0)
        try:
            apply1(c, action)
        except KeyError:  # LOL
            actions.append(action)
    return c

def run(inp):
    c = new_circuit()
    actions = inp.strip().splitlines()
    a = applyall(c, actions)['a']
    replace_b(actions, a)
    c = new_circuit()
    return applyall(c, actions)

real_input = open('inputs/day07.input.txt').read()
print(run(real_input)['a'])  # => 14710
