from aoc.common import *

grid = read_grid()
n = len(grid)

part1 = set()
part2 = set()

for freq in set(np.unique(grid)) - {'.'}:
  for a, b in itertools.combinations(np.argwhere(grid == freq), 2):
    # Part 1
    for coord in [a + (a-b), b - (a-b)]:
      if (coord >= 0).all() and (coord < n).all():
        part1.add(tuple(coord))
    # Part 2
    for slope in [a - b, b - a]:
      coord = a.copy()
      while (coord >= 0).all() and (coord < n).all():
        part2.add(tuple(coord))
        coord += slope

print("Part 1:", len(part1))
print("Part 2:", len(part2))