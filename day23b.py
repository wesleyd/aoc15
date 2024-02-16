#!/usr/bin/env python3

import re

def parse(inp):
    instructions = []
    for line in inp.strip().splitlines():
        instructions.append(re.split(r',? ', line))
    return instructions

class CPU:
    def __init__(self):
        self.reg = {}
        self.reg['a'] = 1
        self.reg['b'] = 0
        self.pc = 0

def run1(cpu, instr):
    op, r = instr[0], instr[1]
    if len(instr) > 2:
        offset = int(instr[2])
    match op:
        case 'hlf':
            cpu.reg[r] //= 2
            cpu.pc += 1
        case 'tpl':
            cpu.reg[r] *= 3
            cpu.pc += 1
        case 'inc':
            cpu.reg[r] += 1
            cpu.pc += 1
        case 'jmp':
            offset = int(r)
            cpu.pc += offset
        case 'jie':
            if cpu.reg[r] % 2 == 0:
                cpu.pc += offset
            else:
                cpu.pc += 1
        case 'jio':
            if cpu.reg[r] == 1:  # Jump if **one**
                cpu.pc += offset
            else:
                cpu.pc += 1

def run(instructions, cpu=None):
    if not cpu:
        cpu = CPU()
    while cpu.pc < len(instructions):
        instr = instructions[cpu.pc]
        run1(cpu, instructions[cpu.pc])
    return cpu

real_input = open('inputs/day23.input.txt').read()
real_instructions = parse(real_input)
print(run(real_instructions).reg['b'])  # => 247
