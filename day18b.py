#!/usr/bin/env python3

example_input = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

def turn_on_corners(grid):
    grid[0][0] = '#'
    grid[0][-1] = '#'
    grid[-1][0] = '#'
    grid[-1][-1] = '#'

def parse(inp):
    grid = [list(line) for line in inp.strip().splitlines()]
    turn_on_corners(grid)
    return grid
example_grid = parse(example_input)

def grid_to_string(grid):
    return '\n'.join([''.join(line) for line in grid])
assert grid_to_string(parse(example_input)) == """
##.#.#
...##.
#....#
..#...
#.#..#
####.#
""".strip()

def at(grid, row, col):
    if row < 0 or len(grid) <= row:
        return '.'
    if col < 0 or len(grid[row]) <= col:
        return '.'
    return grid[row][col]

def num_neighbors_on(g, row, col):
    nn = 0
    for r in [row-1, row, row+1]:
        for c in [col-1, col, col+1]:
            if r == row and c == col:
                continue
            if at(g, r, c) == '#':
                nn += 1
    return nn

def animate1(grid):
    g2 = []
    for row in range(len(grid)):
        line = []
        for col, ch in enumerate(grid[row]):
            nn = num_neighbors_on(grid, row, col)
            if ch == '#' and nn in [2, 3] or ch == '.' and nn == 3:
                line.append('#')
            else:
                line.append('.')
        g2.append(line)
    turn_on_corners(g2)
    return g2
assert grid_to_string(animate1(example_grid)) == """
#.##.#
####.#
...##.
......
#...#.
#.####
""".strip()

def animateN(grid, n=1):
    while n:
        grid = animate1(grid)
        n -= 1
    return grid
assert grid_to_string(animateN(example_grid, 5)) == """
##.###
.##..#
.##...
.##...
#.#...
##...#
""".strip()

def num_on(grid):
    return sum(sum(1 if ch == '#' else 0 for ch in line) for line in grid)
assert num_on(example_grid) == 17
assert num_on(animateN(example_grid, 5)) == 17

real_input = open('inputs/day18.input.txt').read()
real_grid = parse(real_input)
print(num_on(animateN(real_grid, 100)))  # => 1006
