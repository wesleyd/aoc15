#!/usr/bin/env python3

import re

input_ticker = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""

input_sues = open('inputs/day16.input.txt').read()

def parse_sues(inp):
    sues = {}
    for line in inp.strip().splitlines():
        l, rr = line.split(':', 1)
        sue_number = int(re.match(r'Sue (\d+)', l).group(1))
        sue = {}
        for r in rr.split(','):
            thing, ns = r.split(':')
            sue[thing.strip()] = int(ns)
        sues[sue_number] = sue
    return sues

def parse_ticker(inp):
    ticker = {}
    for line in inp.strip().splitlines():
        l, r = line.split(':')
        ticker[l] = int(r)
    return ticker

def possible(ticker, sue):
    for thing, n in ticker.items():
        if thing not in sue:
            continue
        if sue[thing] != n:
            return False
    return True


def apply_ticker(ticker, sues):
    for nsue, sue in sues.items():
        if possible(ticker, sue):
            return nsue

ticker = parse_ticker(input_ticker)
sues = parse_sues(input_sues)
print(apply_ticker(ticker, sues))  # => 213
