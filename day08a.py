#!/usr/bin/env python3

example_input = r"""
""
"abc"
"aaa\"aaa"
"\x27"
"""

def escape(s):
    t = []
    s = list(s[1:-1])
    while s:
        c = s.pop(0)
        if c == '\\':
            d = s.pop(0)
            if d == '"':
                t.append('"')
            elif d == '\\':
                t.append('\\')
            elif d == 'x':
                t.append(chr(int(s.pop(0) + s.pop(0), 16)))
        else:
            t.append(c)
    return ''.join(t)
assert escape('""') == ''
assert escape('"abc"') == 'abc'
assert escape('"\x27"') == "'"
assert escape('"aaa\"aaa"') == 'aaa"aaa'
assert escape('"\\\\zrs\\\\syur"') == '\\zrs\\syur'

def run(inp):
    n = 0
    for s in inp.strip().splitlines():
        n += len(s) - len(escape(s))
    return n
assert run(example_input) == 12

real_input = open('inputs/day08.input.txt').read()
print(run(real_input))  # => 1342
