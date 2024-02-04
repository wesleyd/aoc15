#!/usr/bin/env python3

import hashlib

def collide(inp):
    i = 0
    while True:
        if hashlib.md5((inp + str(i)).encode()).hexdigest().startswith("000000"):
            return i
        i += 1

real_input = "yzbqklnj"

print(collide(real_input))  # => 9962624
