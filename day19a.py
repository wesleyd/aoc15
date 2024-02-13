#!/usr/bin/env python3

example_input = """
H => HO
H => OH
O => HH

HOH
"""

def parse(inp):
    rr, seed = inp.strip().split('\n\n')
    rules = []
    for r in rr.split('\n'):
        a, z = r.split(' => ')
        rules.append((a, z))
    return seed, rules
example_seed, example_rules = parse(example_input)

def fuse_all(seed, rules):
    molecules = set()
    for a, z in rules:
        for i in range(len(seed)-(len(a)-1)):
            if seed[i:i+len(a)] == a:
                molecules.add(seed[:i] + z + seed[i+len(a):])
    return molecules
assert len(fuse_all(example_seed, example_rules)) == 4

real_input = open('inputs/day19.input.txt').read()
real_seed, real_rules = parse(real_input)
print(len(fuse_all(real_seed, real_rules)))  # => 535
