#!/usr/bin/env python3

def two_pairs(lst):
    """Returns true if lst contains two different pairs."""
    n = 0
    i = 0
    while i < len(lst)-3:
        if lst[i] == lst[i+1]:
            n += 1
            break
        i += 1
    if n == 0:
        return False
    j = i + 2
    while j < len(lst)-1:
        if lst[j] == lst[j+1] and lst[j] != lst[i]:
            n += 1
            break
        j += 1
    return n == 2
assert two_pairs('abbceffg')
assert not two_pairs('abbcebbg')
assert two_pairs('ghjaabcc')
assert not two_pairs('abcdefgh')

def to_numbers(s):
   return [ord(c)-ord('a') for c in s]

def from_numbers(lst):
    return ''.join(chr(n+ord('a')) for n in lst)

def straight(lst):
    if isinstance(lst, str):
        lst = to_numbers(lst)
    i = 0
    while i < len(lst)-2:
        if lst[i+1] == lst[i]+1 and lst[i+2] == lst[i]+2:
            return True
        i += 1
    return False
assert straight('hijklmmn')
assert not straight('abbceffg')


forbidden = ['o', 'l', 'i'] + [ord(c) - ord('a') for c in 'oli']
def oli_free(lst):
    for x in lst:
        if x in forbidden:
            return False
    return True
assert oli_free(to_numbers('abcdef'))
assert oli_free('abcdef')
assert not oli_free(to_numbers('abcief'))
assert not oli_free('abcief')

def inc1(s):
    if isinstance(s, str):
        lst = to_numbers(s)
    else:
        lst = s
    i = len(lst)
    while i:
        i -= 1
        lst[i] += 1
        if lst[i] < 26:
            break
        elif lst[i] == 26:
            lst[i] = 0
    if isinstance(s, str):
        return from_numbers(lst)
    return lst
assert inc1('abcdefy') == 'abcdefz'
assert inc1('abcdefz') == 'abcdega'
assert inc1('yzzzzzz') == 'zaaaaaa'

def inc1_oli(lst):
    assert isinstance(lst, list)
    i = 0
    while i < len(lst):
        if lst[i] in forbidden:
            break
        i += 1
    if i == len(lst):
        return inc1(lst)
    else:
        return inc1(lst[:i+1]) + [0] * (len(lst)-i-1)
assert from_numbers(inc1_oli(to_numbers('abcdifgh'))) == 'abcdjaaa'

def inc(s):
    if isinstance(s, str):
        lst = to_numbers(s)
    else:
        lst = s
    inc1(lst)
    while not(two_pairs(lst) and straight(lst) and oli_free(lst)):
        if not two_pairs(lst):
            lst = inc1(lst) # next_two_pair(lst)
        if not straight(lst):
            lst = inc1(lst) # next_straight(lst)
        if not oli_free(s):
            lst = inc1_oli(lst)
    if isinstance(s, str):
        return from_numbers(lst)
    return lst
assert inc('abcdefgz') == 'abcdffaa'
assert inc('abcdhigz') == 'abcdjjaa'

print(inc('hepxcrrq')) # => 'hepxyzz'
