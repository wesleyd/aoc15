#!/usr/bin/env python3

import json

def sum_numbers(j):
    if isinstance(j, int):
        return j
    elif isinstance(j, list):
        return sum(sum_numbers(x) for x in j)
    elif isinstance(j, dict):
        if "red" in j or "red" in j.values():
            return 0
        else:
            return sum_numbers(list(j)) + sum_numbers(list(j.values()))
    else:
        return 0

assert sum_numbers(json.loads('[1,2,3]')) == 6
assert sum_numbers(json.loads('{"a":2,"b":4}')) == 6
assert sum_numbers(json.loads('[[[3]]]')) == 3
assert sum_numbers(json.loads('{"a":{"b":4},"c":-1}')) == 3
assert sum_numbers(json.loads('{"a":[-1,1]}')) == 0
assert sum_numbers(json.loads('[-1,{"a":1}]')) == 0
assert sum_numbers(json.loads('[]')) == 0
assert sum_numbers(json.loads('{}')) == 0
assert sum_numbers(json.loads('[1,{"c":"red","b":2},3]'))

real_input = open('inputs/day12.input.txt').read()
print(sum_numbers(json.loads(real_input)))  # => 96852
