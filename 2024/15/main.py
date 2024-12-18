from aoc.common import *

dirs = {
    "<": complex(0, -1),
    ">": complex(0, 1),
    "^": complex(-1, 0),
    "v": complex(1, 0)
}

grid, moves = read_input(
    delim="\n\n",
)

np_grid = read_grid(text=grid)
moves = moves.replace("\n", "")

grid = dict()
for (j,i), value in np.ndenumerate(np_grid):
  if value == "@":
    robot = complex(j,i)

  if value != ".":
    grid[complex(j,i)] = value

def swap(pos, new_pos, o):
  del grid[pos]
  grid[new_pos] = o
  return True

def move_object(pos, d):
  if pos not in grid:
    return True

  o = grid[pos]
  if o == "#":
    return False

  new_pos = pos + d
  if (new_pos not in grid) or move_object(new_pos, d):
    return swap(pos, new_pos, o)

  return False

def solve(robot, target):
  for move in moves:
    d = dirs[move]
    if move_object(robot, d):
      robot += d

  s = 0
  for k, v in grid.items():
    if v == target:
      s += int(100 * abs(k.real) + abs(k.imag))

  return s

print("Part 1:", solve(robot, "O"))

grid = dict()
for (j,i), value in np.ndenumerate(np_grid):
  if value == "@":
    robot = complex(j,2*i)
    grid[robot] = "@"
  elif value == "O":
    grid[complex(j,2*i)] = "["
    grid[complex(j,2*i+1)] = "]"
  elif value == "#":
    grid[complex(j,2*i)] = "#"
    grid[complex(j,2*i+1)] = "#"

def move_object(pos, d):
  global grid

  if pos not in grid:
    return True

  o = grid[pos]
  if o == "#":
    return False

  new_pos = pos + d

  # Left or right works as before
  if (d.real == 0) and move_object(new_pos, d):
    return swap(pos, new_pos, o)

  if d.real != 0:
    backup_grid = dict(grid)

    if (o == "["):
      if move_object(new_pos, d) and move_object(new_pos + 1j, d):
        swap(pos, new_pos, o)
        swap(pos + 1j, new_pos + 1j, "]")
        return True
    elif (o == "]"):
      if move_object(new_pos, d) and move_object(new_pos - 1j, d):
        swap(pos, new_pos, o)
        swap(pos - 1j, new_pos - 1j, "[")
        return True
    elif move_object(new_pos, d):
      return swap(pos, new_pos, o)

    grid = backup_grid

  return False

print("Part 2:", solve(robot, "["))