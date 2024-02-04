#!/usr/bin/env python3

def count(parens: str) -> int:
    n = 0
    for c in parens:
        if c == '(':
            n += 1
        elif c == ')':
            n -= 1
    return n
assert count("(())") == 0

print(count(open('inputs/day01.input.txt').read()))
