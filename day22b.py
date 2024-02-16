#!/usr/bin/env python3

import copy
import math
import re

from collections import namedtuple
from dataclasses import dataclass
from heapdict import heapdict
from enum import Enum
from typing import Dict

LOUD=False

def say(*args, **kwargs):
    if LOUD:
        print(*args, **kwargs)

example_input = """
Hit Points: 13
Damage: 8
"""

Boss = namedtuple('Boss', ['hp', 'damage'])

def parse_boss(inp):
    hp = int(re.search(r'Hit Points: (\d+)', inp).group(1))
    damage = int(re.search(r'Damage: (\d+)', inp).group(1))
    return Boss(hp=hp, damage=damage)
example_boss = parse_boss(example_input)

class Spell(Enum):
    MAGIC_MISSILE = 1
    DRAIN = 2
    SHIELD = 3
    POISON = 4
    RECHARGE = 5

spell_cost: Dict[Spell, int] = {
    Spell.MAGIC_MISSILE: 53,
    Spell.DRAIN: 73,
    Spell.SHIELD: 113,
    Spell.POISON: 173,
    Spell.RECHARGE: 229,
}
all_spells = list(spell_cost.keys())

@dataclass(unsafe_hash=True)
class State:
    total_cost: int
    hp: int
    mana: int
    boss_hp: int
    boss_damage: int
    poison_timer: int
    shield_timer: int
    recharge_timer: int
    armor: int

def start(*, hp: int, mana: int, boss: Boss) -> State:
    state = State(
        total_cost = 0,
        hp = hp,
        mana = mana,
        boss_hp = boss.hp,
        boss_damage = boss.damage,
        poison_timer = 0,
        shield_timer = 0,
        recharge_timer = 0,
        armor = 0)
    return state

def is_spell_allowed(state:State, spell):
    if spell == Spell.SHIELD and state.shield_timer > 0:
        return False
    if spell == Spell.POISON and state.poison_timer > 0:
        return False
    if spell == Spell.RECHARGE and state.recharge_timer > 0:
        return False
    return True

def advance_timers(state: State):
    if state.shield_timer > 0:
        state.shield_timer -= 1
        if state.shield_timer == 0:
            say(f'Shield wears off.')
            state.armor -= 7
        else:
            say(f"Shield's timer is now {state.shield_timer}")
    if state.recharge_timer > 0:
        state.recharge_timer -= 1
        state.mana += 101
        say(f'Recharge provides 101 mana; its timer is now {state.recharge_timer}')
        if state.recharge_timer == 0:
            say(f'Recharge wears off.')
    if state.poison_timer > 0:
        state.poison_timer -= 1
        state.boss_hp -= 3
        say(f'Poison deals 3 damage; its timer is now {state.poison_timer}')
        if state.poison_timer == 0:
            say(f'Poison wears off')

def cast(state: State, spell: Spell):
    cost = spell_cost[spell]
    mana_before = state.mana
    state.mana -= spell_cost[spell]
    state.total_cost += cost
    match spell:
        case Spell.MAGIC_MISSILE:
            say(f'Player casts Magic Missile ${cost}, dealing 4 damage')
            state.boss_hp -= 4
        case Spell.DRAIN:
            say(f'Player casts Drain, dealing 2 damage, and healing 2 hit points')
            state.boss_hp -= 2
            state.hp += 2
        case Spell.SHIELD:
            say(f'Player casts Shield ${cost}, increasing armor by 7')
            state.armor += 7
            assert state.shield_timer == 0, state
            state.shield_timer = 6
        case Spell.POISON:
            say(f'Player casts Poison ${cost}.')
            assert state.poison_timer == 0
            state.poison_timer = 6
        case Spell.RECHARGE:
            say(f'Player casts Recharge ${cost}.')
            assert state.recharge_timer == 0
            state.recharge_timer += 5

def move(state: State, spell: Spell) -> State:
    state = copy.deepcopy(state)
    say('-- Player turn --')
    say(f'- Player has {state.hp} hit points, {state.armor} armor, {state.mana} mana, spent ${state.total_cost}')
    say(f'- Boss has {state.boss_hp} hit points')
    state.hp -= 1
    say(f'You lose one hp, because you just do, hp now {state.hp}')
    if state.hp <= 0:
        say(f'That one hp loss killed you. You lose.')
        return
    advance_timers(state)
    if not is_spell_allowed(state, spell):
        return
    cast(state, spell)
    if state.mana < 0:
        say(f'Not a valid spell: mana < 0; return')
        return
    if state.boss_hp <= 0:
        say(f'You killed the boss ({state.boss_hp}). You win.')
        return state
    say(f'-- At the end of your turn, you have {state.hp}, boss has {state.boss_hp}. You have spent ${state.total_cost}')
    say()
    say('-- Boss turn --')
    say(f'- Player has {state.hp} hit points, {state.armor} armor, {state.mana} mana, spent ${state.total_cost}')
    say(f'- Boss has {state.boss_hp} hit points')
    advance_timers(state)
    if state.boss_hp <= 0:
        say(f'That killed the boss ({state.boss_hp}). You win.')
        return state
    damage = state.boss_damage - state.armor
    if state.armor:
        say(f'Boss attacks for {state.boss_damage} - {state.armor} = {damage} damage!')
    else:
        say(f'Boss attacks for {damage}!')
    state.hp -= damage
    if state.hp <= 0:
        say('The boss killed you. The boss wins.')
        return
    say(f'-- At the end of boss turn, you have {state.hp}, boss has {state.boss_hp}. You have spent ${state.total_cost}')
    say()
    return state

def i_won(state):
    say(f'Total cost ${state.total_cost}')
    return state.hp > 0 and state.boss_hp <= 0
def boss_won(state):
    return state.boss_hp > 0 and state.hp <= 0

def print_winning_path(st, prev):
    path = []
    spell = None
    while st:
        if spell:
            path.append(f'  {spell}')
        path.append(f'{st}')
        st, spell = prev.get(st, (None, None))
    for line in reversed(path):
        print(line)

def replay_winning_game(st, prev):
    path = []
    spell = None
    while st:
        path.append((st, spell))
        st, spell = prev.get(st, (None, None))
    global LOUD
    LOUD = True
    path.reverse()
    st = path[0][0]
    for _, spell in path:
        if spell:
            st = move(st, spell)
    LOUD = False

def play(hp, mana, boss):
    first = start(hp=hp, mana=mana, boss=boss)
    future = heapdict()
    prev = {}
    future[first] = 0
    while future:
        st, _ = future.popitem()
        if i_won(st):
            #replay_winning_game(st, prev)
            return st
        elif boss_won(st):
            continue
        # On each of your turns, you must select one of your spells to cast.
        # If you cannot afford to cast any spell, you lose.
        for spell in all_spells:
            st2 = move(st, spell)
            if not st2:
                continue
            future[st2] = st2.total_cost
            prev[st2] = (st, spell)
    return lowest

real_input = open('inputs/day22.input.txt').read()
real_boss = parse_boss(real_input)
print(play(50, 500, real_boss).total_cost)  # => 1289
