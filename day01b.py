#!/usr/bin/env python3

def first_basement(parens: str) -> int:
    n = 0
    for i, c in enumerate(parens):
        if c == '(':
            n += 1
        elif c == ')':
            n -= 1
        if n < 0:
            return i+1
assert first_basement(")") == 1
assert first_basement("()())") == 5

print(first_basement(open('inputs/day01.input.txt').read()))
