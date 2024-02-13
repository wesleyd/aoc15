#!/usr/bin/env python3

import functools
import itertools
import operator

puzzle_input = 33100000

biggest = 2
primes = [2]
def is_prime(n):
    global biggest, primes
    def divisible_by_known_primes(n):
        for p in primes:
            if n % p == 0:
                return True
        return False
    while biggest*biggest < n:
        biggest += 1
        if not divisible_by_known_primes(biggest):
            primes.append(biggest)
    return not divisible_by_known_primes(n)
assert not is_prime(10_000)
assert primes[:25] == [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

def prime_factors(n):
    if is_prime(n):
        return []
    factors = []
    for p in reversed(primes):
        while n % p == 0:
            factors.append(p)
            n /= p
    return factors
assert prime_factors(60) == [5, 3, 2, 2]

def factors(n):
    ff = set()
    pf = prime_factors(n)
    for i in range(len(pf)):
        for combo in itertools.combinations(pf, i):
            ff.add(functools.reduce(operator.mul, combo, 1))
    ff.add(n)
    return ff
assert factors(60) == set([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60])
assert factors(100) == set([1, 2, 4, 5, 10, 20, 25, 50, 100])
assert factors(128) == set([1, 2, 4, 8, 16, 32, 64, 128])

def ngifts(house):
    n = 0
    ff = list(factors(house))
    ff.sort(reverse=True)
    for f in ff:
        if house / f > 50:
            break
        n += 11*f
    return n

house = 1
while True:
    n = ngifts(house)
    if n >= puzzle_input:
        break
    house += 1
print(house)  # => 786240
