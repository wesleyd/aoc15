#!/usr/bin/env python3

def wrap(inp):
    paper = 0
    for line in inp.splitlines():
        w, d, h = [int(x) for x in line.strip().split('x')]
        faces = [ w*d, w*h, h*d ]
        paper += 2 * sum(faces) + min(faces)
    return paper
assert wrap("2x3x4") == 58
assert wrap("1x1x10") == 43

real_input = open('inputs/day02.input.txt').read()
print(wrap(real_input))
