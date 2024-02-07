#!/usr/bin/env python3

example_input = r"""
""
"abc"
"aaa\"aaa"
"\x27"
"""

def encode(s):
    t = ['"']
    for c in s:
        if c == '"':
            t.append('\\')
            t.append('"')
        elif c == '\\':
            t.append('\\')
            t.append('\\')
        else:
            t.append(c)
    t.append('"')
    return t
assert len(encode('""')) == 6
assert len(encode('"abc"')) == 9
assert len(encode(r'"aaa\"aaa"')) == 16
assert len(encode(r'"\x27"')) == 11

def run(inp):
    n = 0
    for s in inp.strip().splitlines():
        n += len(encode(s)) - len(s)
    return n
assert run(example_input) == 19

real_input = open('inputs/day08.input.txt').read()
print(run(real_input))  # => 2074
