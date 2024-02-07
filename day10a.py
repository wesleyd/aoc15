#!/usr/bin/env python3

def expand1(s):
    t = []
    i = 0
    while i < len(s):
        n = 1
        c = s[i]
        i += 1
        while i < len(s) and s[i] == c:
            i += 1
            n += 1 
        t.append(f'{n}{c}')
    return ''.join(t)
assert expand1('1') == '11'
assert expand1('11') == '21'
assert expand1('21') == '1211'
assert expand1('1211') == '111221'
assert expand1('111221') == '312211'

def expand(s, n):
    while n:
        s = expand1(s)
        n -= 1
    return s
assert expand('1', 5) == '312211'

real_input = '1113122113'
print(len(expand(real_input, 40)))  # => 360154
