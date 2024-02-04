#!/usr/bin/env python3

import hashlib

example_input = "abcdef"

def collide(inp):
    i = 0
    while True:
        if hashlib.md5((inp + str(i)).encode()).hexdigest().startswith("00000"):
            return i
        i += 1

assert collide(example_input) == 609043

real_input = "yzbqklnj"

print(collide(real_input))  # => 282749
