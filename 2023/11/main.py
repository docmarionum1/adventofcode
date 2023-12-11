from aoc.common import *

grid = read_grid()

missing_rows = set(np.arange(grid.shape[0])).difference(np.unique(np.argwhere(grid == "#")[:,0]))
missing_cols = set(np.arange(grid.shape[1])).difference(np.unique(np.argwhere(grid == "#")[:,1]))

def solve(multiplier):
  s = 0

  for (ay, ax), (by, bx) in list(itertools.combinations(np.argwhere(grid == "#"), 2)):
    ax, bx = sorted([ax, bx])
    ay, by = sorted([ay, by])

    mr = len([r for r in missing_rows if r > ay and r < by])
    mc = len([c for c in missing_cols if c > ax and c < bx])

    s += (bx - ax) + (by - ay) + (mr + mc) * multiplier

  return s

print("Part 1:", solve(1))
print("Part 2:", solve(999999))