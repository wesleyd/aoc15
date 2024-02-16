#!/usr/bin/env python3

import copy
import re

from collections import namedtuple
from dataclasses import dataclass
from heapdict import heapdict
from enum import Enum
from typing import Dict

def say(*args, **kwargs):
    #print(*args, **kwargs)
    pass

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
    NO_SPELL = 0
    MAGIC_MISSILE = 1
    DRAIN = 2
    SHIELD = 3
    POISON = 4
    RECHARGE = 5

spell_cost: Dict[Spell, int] = {
    Spell.NO_SPELL: 0,
    Spell.MAGIC_MISSILE: 53,
    Spell.DRAIN: 73,
    Spell.SHIELD: 113,
    Spell.POISON: 173,
    Spell.RECHARGE: 229,
}

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

def allowed_spells(state: State) -> Spell:
    """Yields all the possible moves from state"""
    if state.hp <= 0 or state.boss_hp <= 0:
        return
    yield Spell.NO_SPELL
    if state.mana > spell_cost[Spell.MAGIC_MISSILE]:
        yield Spell.MAGIC_MISSILE
    if state.mana > spell_cost[Spell.DRAIN]:
        yield Spell.DRAIN
    if state.shield_timer == 0 and state.mana > spell_cost[Spell.SHIELD]:
        yield Spell.SHIELD
    if state.poison_timer == 0 and state.mana > spell_cost[Spell.POISON]:
        yield Spell.POISON
    if state.recharge_timer == 0 and state.mana > spell_cost[Spell.RECHARGE]:
        yield Spell.RECHARGE

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
    if spell == Spell.NO_SPELL:
        return
    cost = spell_cost[spell]
    mana_before = state.mana
    state.mana -= spell_cost[spell]
    assert state.mana >= 0, (state, spell)
    state.total_cost += cost
    match spell:
        case Spell.MAGIC_MISSILE:
            say(f'Player casts Magic Missile, dealing 4 damage')
            state.boss_hp -= 4
        case Spell.DRAIN:
            say(f'Player casts Drain, dealing 2 damage, and healing 2 hit points')
            state.boss_hp -= 2
            state.hp += 2
        case Spell.SHIELD:
            say(f'Player casts Shield, increasing armor by 7')
            state.armor += 7
            assert state.shield_timer == 0
            state.shield_timer = 6
        case Spell.POISON:
            say(f'Player casts Poison.')
            assert state.poison_timer == 0
            state.poison_timer = 6
        case Spell.RECHARGE:
            say(f'Player casts Recharge.')
            assert state.recharge_timer == 0
            state.recharge_timer += 5

def move(state: State, spell: Spell) -> State:
    state = copy.deepcopy(state)
    say('-- Player turn --')
    say(f'- Player has {state.hp} hit points, {state.armor} armor, {state.mana} mana')
    say(f'- Boss has {state.boss_hp} hit points')
    advance_timers(state)
    if state.boss_hp <= 0:
        say(f'That killed the boss ({state.boss_hp}). You win.')
        return state
    cast(state, spell)
    if state.boss_hp <= 0:
        say(f'You killed the boss ({state.boss_hp}). You win.')
        return state
    say()
    say('-- Boss turn --')
    say(f'- Player has {state.hp} hit points, {state.armor} armor, {state.mana} mana')
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
    say()
    return state

def i_won(state):
    say(f'Total cost ${state.total_cost}')
    return state.hp > 0 and state.boss_hp <= 0
def boss_won(state):
    return state.boss_hp > 0 and state.hp <= 0

def play_example1():
    state = start(hp=10, mana=250, boss=example_boss)
    state = move(state, Spell.POISON)
    state = move(state, Spell.MAGIC_MISSILE)
    return state
assert i_won(play_example1())

def play_example2():
    state = start(hp=10, mana=250, boss=Boss(hp=14, damage=8))
    state = move(state, Spell.RECHARGE)
    state = move(state, Spell.SHIELD)
    state = move(state, Spell.DRAIN)
    state = move(state, Spell.POISON)
    state = move(state, Spell.MAGIC_MISSILE)
    return state
assert i_won(play_example2())

def play(hp, mana, boss):
    future = heapdict()
    future[start(hp=hp, mana=mana, boss=boss)] = 0
    while future:
        st, _ = future.popitem()
        if i_won(st):
            say(f'Win! ${st.total_cost} ({st})')
            return st
        for spell in allowed_spells(st):
            st2 = move(st, spell)
            future[st2] = st2.total_cost

assert play(10, 250, example_boss).total_cost == 226
assert play(10, 250, Boss(hp=14, damage=8)).total_cost == 641

real_input = open('inputs/day22.input.txt').read()
real_boss = parse_boss(real_input)
print(play(50, 500, real_boss).total_cost)  # => 953
