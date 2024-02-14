#!/usr/bin/env python3

import re
import math

from collections import namedtuple

example_input = """
Hit Points: 12
Damage: 7
Armor: 2
"""

Player = namedtuple('Player', ['hp', 'damage', 'armor'])

def parse_player(inp):
    return Player(
        hp=int(re.search(r'Hit Points: (\d+)', inp).group(1)),
        damage=int(re.search(r'Damage: (\d+)', inp).group(1)),
        armor=int(re.search(r'Armor: (\d+)', inp).group(1))
    )
assert parse_player(example_input) == Player(12, 7, 2)

real_input = open('inputs/day21.input.txt').read()
boss = parse_player(real_input)


shop_input = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

Item = namedtuple('Item', ['name', 'plus', 'cost', 'damage', 'armor'])
Shop = namedtuple('Shop', ['weapons', 'armors', 'rings'])

def parse_shop(inp):
    nothing = Item('Nothing', 0, 0, 0, 0)
    weapons = []
    armors = [nothing]
    rings = [nothing]
    curr = None
    for line in inp.strip().splitlines():
        if 'Weapons:' in line:
            curr = weapons
            continue
        elif 'Armor:' in line:
            curr = armors
            continue
        elif 'Rings:' in line:
            curr = rings
            continue
        m = re.match(r'([A-Za-z]+)\s+(\+\d+)?\s+(\d+)\s+(\d+)\s+(\d+)', line)
        if m:
            g = m.groups()
            plus = int(g[1]) if g[1] else 0
            item = Item(name=g[0], plus=plus, cost=int(g[2]), damage=int(g[3]), armor=int(g[4]))
            curr.append(item)
    rings.append(nothing)
    return Shop(weapons=weapons, armors=armors, rings=rings)
shop = parse_shop(shop_input)

def wear(weapon, armors, rings):
    armor, damage = 0, 0
    if weapon:
        damage += weapon.damage
    if armors:
        armor += armors.armor
    for ring in rings:
        if ring.name == "Damage":
            damage += ring.plus
        elif ring.name == "Defense":
            armor += ring.plus
        elif ring.name == "Nothing":
            pass
        else:
            assert False, f'bad ring name {ring}'
    return Player(100, damage, armor)

def play(me, them):
    """Returns True if I win."""
    hp_me, hp_them = me.hp, them.hp
    my_score = me.damage - them.armor
    if my_score <= 0:
        my_score = 1
    their_score = them.damage - me.armor
    if their_score <= 0:
        their_score = 1
    # I can definitely survive this many rounds
    rounds = (hp_me-1) // their_score
    hp_me -= their_score * rounds
    assert hp_me > 0, (hp_me, their_score, rounds)
    # Can they?
    hp_them -= my_score * rounds
    if hp_them <= 0:
        return True
    while True:
        hp_them -= my_score
        #print(f'I deal {my_score} damage, the  boss goes down to {hp_them} hit points.')
        if hp_them <= 0:
            return True
        hp_me -= their_score
        #print(f'The boss deals {their_score} damage, I go down to {hp_me} hit points.')
        if hp_me <= 0:
            return False

def shop_combos(shop):
    for weapon in shop.weapons:
        for armor in shop.armors:
            for i in range(len(shop.rings)):
                for j in range(i+1, len(shop.rings)):
                    ring1, ring2 = shop.rings[i], shop.rings[j]
                    cost = weapon.cost + armor.cost + ring1.cost + ring2.cost
                    #print(f'${cost} {weapon.name}+{weapon.damage} {armor.name}+{armor.armor} {ring1.name}+{ring1.plus} {ring2.name}+{ring2.plus}') 
                    yield cost, wear(weapon, armor, [ring1, ring2])

def run(shop, boss):
    dearest = -math.inf
    for cost, me in shop_combos(shop):
        #print(f'Me={me} v Boss={boss} : ${cost}', end='')
        if play(me, boss):
            #print('=> Win')
            continue
        #print('=> Lose')
        if cost > dearest:
            #print(f'{me} => ${cost}')
            dearest = cost
    return dearest
print(run(shop, boss))  # It is not $75 ; it is not $0 either, darnit. Not $178 either !!!
