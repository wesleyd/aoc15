#!/usr/bin/env python3

def bow(inp):
    ribbon = 0
    for line in inp.splitlines():
        w, d, h = [int(x) for x in line.strip().split('x')]
        ribbon += 2*min(w+d, w+h, h+d) + w*d*h
    return ribbon
assert bow("2x3x4") == 34
assert bow("1x1x10") == 14

real_input = open('inputs/day02.input.txt').read()
print(bow(real_input))
