from aoc.common import *

def read_schematic(schematic):
  grid = read_grid(text=schematic)
  if (grid[0] == '#').all():
    return "lock", (grid == '#').sum(axis=0) - 1
  else:
    return "key", (grid == '#').sum(axis=0) - 1

schematics = read_input(
    delim="\n\n",
    mapper=read_schematic,
)

locks = [s[1] for s in schematics if s[0] == "lock"]
keys = [s[1] for s in schematics if s[0] == "key"]

count = 0
for l, k in itertools.product(locks, keys):
  if ((l + k) <= 5).all():
    count += 1

print("Part 1:", count)