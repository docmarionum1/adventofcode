from aoc.common import *

grid = read_grid()

def north(grid):
  for i in range(1, len(grid)):
    rocks = np.argwhere(grid[i] == 'O').flatten()

    g = np.vstack([["#"]*len(rocks), grid[0:i,rocks]])
    m = (np.indices(g.shape)[0] * (g != '.')).max(axis=0)
    grid[i,rocks] = '.'
    grid[m,rocks] = 'O'

def load(grid):
  return ((grid == 'O').sum(axis=1) * np.arange(len(grid), 0, -1)).sum()

def part1(grid):
  grid = grid.copy()
  north(grid)
  return load(grid)

# Part 1
print("Part 1:", part1(grid))

def cycle(grid):
  for i in range(4):
    north(grid)
    grid = np.rot90(grid, axes=(1, 0))

  return grid

def part2(grid):
  grid = grid.copy()
  numbers = []
  string = ""

  for i in range(500):
    l = load(grid)
    numbers.append(l)
    string = string + "," + str(l)
    grid = cycle(grid)

    for j in range(i-2, 0, -1):
      substring = ",".join([str(x) for x in numbers[j:i]])
      if string.count(substring) > 1:
        if string.count(substring + "," + substring) > 0:
          pattern = numbers[j:i]
          start = pattern[0]
          return pattern[(1000000000 - start) % len(pattern)]
      else:
        break

print("Part 2:", part2(grid))