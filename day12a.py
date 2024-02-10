#!/usr/bin/env python3

import re

def sum_numbers(s):
    return sum(int(x) for x in re.findall(r'-?\d+', s))

assert sum_numbers('[1,2,3]') == 6
assert sum_numbers('{"a":2,"b":4}') == 6
assert sum_numbers('[[[3]]]') == 3
assert sum_numbers('{"a":{"b":4},"c":-1}') == 3
assert sum_numbers('{"a":[-1,1]}') == 0
assert sum_numbers('[-1,{"a":1}]') == 0
assert sum_numbers('[]') == 0
assert sum_numbers('{}') == 0

real_input = open('inputs/day12.input.txt').read()
print(sum_numbers(real_input)) # => 156366
