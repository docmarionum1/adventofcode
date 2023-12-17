from aoc.common import *

grid = read_grid(text=r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""")

grid = read_grid()

h,w = grid.shape
mi,mj = h-1,w-1


def part1(start = (0,0,"r")):
  to_visit = [start]
  counts = np.zeros(grid.shape)
  visited = {}

  while to_visit:
    i, j, d = to_visit.pop()

    if (i,j,d) in visited:
      continue

    if i < 0 or j < 0 or i >= grid.shape[0] or j >= grid.shape[1]:
      continue

    visited[(i,j,d)] = True

    c = grid[i,j]
    counts[i,j] += 1

    if d == "r":
      if c in ['/', '|']:
        to_visit.append((i-1, j, "u"))
      if c in ['\\', '|']:
        to_visit.append((i+1, j, "d"))
      if c in ['.', '-']:
        to_visit.append((i,j+1,d))

    if d == "l":
      if c in ['/', '|']:
        to_visit.append((i+1, j, "d"))
      if c in ['\\', '|']:
        to_visit.append((i-1, j, "u"))
      if c in ['.', '-']:
        to_visit.append((i,j-1,d))

    if d == "u":
      if c in ['/', '-']:
        to_visit.append((i, j+1, "r"))
      if c in ['\\', '-']:
        to_visit.append((i, j-1, "l"))
      if c in ['.', '|']:
        to_visit.append((i-1,j,d))

    if d == "d":
      if c in ['\\', '-']:
        to_visit.append((i, j+1, "r"))
      if c in ['/', '-']:
        to_visit.append((i, j-1, "l"))
      if c in ['.', '|']:
        to_visit.append((i+1,j,d))

  return (counts > 0).sum()


def part2():
  m = 0

  for i in range(h):
    m = max(m, part1((i,0,"r")), part1((i,mj,"l")))

  for j in range(w):
    m = max(m, part1((0,j,"d")), part1((mi,j,"u")))

  return m


print("Part 1:", part1())
print("Part 2:", part2())