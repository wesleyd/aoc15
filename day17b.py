#!/usr/bin/env python3

import math

example_input = """
20
15
10
5
5
"""

def parse(inp):
    containers = [int(x) for x in inp.strip().splitlines()]
    containers.sort(reverse=True)
    return containers
example_containers = parse(example_input)

real_input = open('inputs/day17.input.txt').read()
real_containers = parse(real_input)

def pack(containers, goal):
    fewest = math.inf
    arrangements = []
    def helper(filled, i):
        nonlocal fewest, arrangements
        if len(filled) > fewest:
            return
        n = sum(filled)
        if n > goal:
            return
        if n == goal:
            if len(filled) < fewest:
                fewest = len(filled)
                arrangements = [filled]
            elif len(filled) == fewest:
                arrangements.append([filled])
        elif i < len(containers):
            helper(filled+[containers[i]], i+1)
            helper(filled, i+1)
    helper([], 0)
    return len(arrangements)
assert pack(example_containers, 25) == 3

print(pack(real_containers, 150)) # => 57
