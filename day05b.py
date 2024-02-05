#!/usr/bin/env python3

def paired(s):
    for i in range(len(s)-2):
        if s[i:i+2] in s[i+2:]:
            return True
    return False

def between(s):
    for i in range(len(s)-2):
        if s[i] == s[i+2]:
            return True
    return False

def nice(s):
    return paired(s) and between(s)

assert nice("qjhvhtzxzqqjkmpb")
assert nice("xxyxx")
assert not nice("uurcxstgmygtbstg")
assert not nice("ieodomkazucvgmuy")

def run(inp):
    return sum(1 if nice(s) else 0 for s in inp.splitlines())

real_input = open('inputs/day05.input.txt').read().strip()

print(run(real_input)) # => it is NOT 53
