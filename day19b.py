#!/usr/bin/env python3

import math

example_input = """
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
"""

def parse(inp):
    rr, goal = inp.strip().split('\n\n')
    rules = []
    for r in rr.split('\n'):
        a, z = r.split(' => ')
        rules.append((a, z))
    rules.sort(key=lambda rule: len(rule[1]), reverse=True)
    return rules, goal
example_rules, example_goal = parse(example_input)

def findall(s, sub, start=0):
    start -= 1
    while True:
        start = s.find(sub, start+1)
        if start < 0:
            return
        yield start
assert list(findall('abc', 'b')) == [1]
assert list(findall('abbc', 'b')) == [1, 2]
assert list(findall('bbabbbcbb', 'bb')) == [0, 3, 4, 7]

def run_backwards(rules, s, goal='e'):
    fewest_steps = math.inf
    def helper(s, n):
        nonlocal fewest_steps
        if n >= fewest_steps:
            return
        if s == goal:
            fewest_steps = n
            yield n
        if goal in s:
            return
        for a, z in rules:
            for i in findall(s, z):
                t = s[:i] + a + s[i+len(z):]
                yield from helper(t, n+1)
    for n in helper(s, 0):
        return n
assert run_backwards(example_rules, 'HOH') == 3
assert run_backwards(example_rules, example_goal) == 6

real_input = open('inputs/day19.input.txt').read()
real_rules, real_goal = parse(real_input)
print(run_backwards(real_rules, real_goal))  # => 212
