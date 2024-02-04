#!/usr/bin/env python3

def nice(s):
    nvowels = 0
    prev = None
    double = False
    for c in s:
        if c in 'aeiou':
            nvowels += 1
        if not prev:
            prev = c
            continue
        if c == prev:
            double = True
        cc = prev + c
        if cc in ('ab', 'cd', 'pq', 'xy'):
            return False
        prev = c
    return double and nvowels >= 3

assert nice("ugknbfddgicrmopn")
assert nice("aaa")
assert not nice("jchzalrnumimnmhp")
assert not nice("haegwjzuvuyypxyu")
assert not nice("dvszwmarrgswjxmb")

def run(inp):
    return sum(1 if nice(s) else 0 for s in inp.splitlines())

real_input = open('inputs/day05.input.txt').read().strip()

print(run(real_input)) # => 258
