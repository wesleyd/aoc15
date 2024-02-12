#!/usr/bin/env python3

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
    def helper(filled, i):
        n = sum(filled)
        if n == goal:
            yield filled
        if i < len(containers) and n < goal:
            yield from helper(filled+[containers[i]], i+1)
            yield from helper(filled, i+1)
    return sum(1 for _ in helper([], 0))

assert pack(example_containers, 25) == 4

print(pack(real_containers, 150)) # => 654
