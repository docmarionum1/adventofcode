from aoc.common import *

grid = read_grid()

STARTING_LOC = tuple(np.argwhere(grid == '^')[0])
STARTING_DIR = '^'

dirs = {
    '^': (-1, 0, '>'),
    'v': (1, 0, '<'),
    '<': (0, -1, '^'),
    '>': (0, 1, 'v'),
}

def get_next(grid, loc, d):
  j, i, n = dirs[d]
  next_loc = (loc[0] + j, loc[1] + i)

  if next_loc[0] < 0 or next_loc[1] < 0:
      raise IndexError

  return next_loc, n, grid[next_loc]

def move(grid, loc, d):
  next_loc, next_dir, next_val = get_next(grid, loc, d)

  if next_val == "#":
    return loc, next_dir
  else:
    return next_loc, d

def process(grid, loc, direction, visited_with_dir):
  while True:
    visited_with_dir.add(loc + (direction,))
    try:
      loc, direction = move(grid, loc, direction)
    except IndexError:
      break
    if loc + (direction,) in visited_with_dir:
      raise ValueError

  return visited_with_dir

part_1_visited_with_dir = process(
    grid.copy(), STARTING_LOC, STARTING_DIR, set()
)
part_1_answer = len(set((j,i) for (j,i,d) in part_1_visited_with_dir))
print("Part 1:", part_1_answer)

def part2(grid):
  loc = STARTING_LOC
  direction = STARTING_DIR

  visited = set()
  visited_with_dir = set()

  obstructions = set()

  for _ in tqdm(range(len(part_1_visited_with_dir)-1)):
    visited.add(loc)
    visited_with_dir.add(loc + (direction,))

    # Figure out if the next location is eligible to be obstructed
    try:
      next_loc, next_dir, next_val = get_next(grid, loc, direction)
    except IndexError:
      break

    # Try adding an obstruction in the next location
    if (next_loc not in visited) and (next_val == '.'):
      grid[next_loc] = '#'

      try:
        process(grid, loc, direction, visited_with_dir.copy())
      except ValueError:
        obstructions.add(next_loc)

      grid[next_loc] = '.'

    # Move to the next location in the original path
    loc, direction = move(grid, loc, direction)

  return obstructions

print("Part 2:", len(part2(grid.copy())))