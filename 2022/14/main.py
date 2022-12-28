import numpy as np
import itertools

def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

traces = open('input.txt').read().splitlines()

def make_grid(part2):
  corners = [tuple(map(int, c.split(","))) for c in ' -> '.join(traces).split(' -> ')]
  ys = np.array([y for x,y in corners])
  max_y = ys.max()
  xs = np.array([x for x,y in corners])
  min_x, max_x = xs.min()-max_y, xs.max()+max_y

  # Part 2
  if part2:
    max_y += 2

  grid = np.zeros((max_y+1, max_x - min_x+1))

  if part2:
    grid[max_y] = np.ones(max_x - min_x + 1)

  for trace in traces:
    corners = [tuple(map(int, c.split(","))) for c in trace.split(" -> ")]
    for a, b in pairwise(corners):
      x1, x2 = sorted([a[0], b[0]])
      y1, y2 = sorted([a[1], b[1]])
      for i in range(x1, x2+1):
        for j in range(y1, y2+1):
          grid[j,i-min_x] = 1

  start = (500 - min_x, 0)

  return grid, start

def place_sand(grid, start):
  pos = list(start)
  while pos[1] < (grid.shape[0]-1):
    if grid[pos[1]+1, pos[0]] == 0:
      pos[1] += 1
    elif grid[pos[1]+1, pos[0]-1] == 0:
      pos[0] -= 1
      pos[1] += 1
    elif grid[pos[1]+1, pos[0]+1] == 0:
      pos[0] += 1
      pos[1] += 1
    else:
      grid[pos[1], pos[0]] = 1
      if pos[1] == start[1]:
        return False
      return True

  return False

def solve(part2):
  grid, start = make_grid(part2)
  count = 0
  while place_sand(grid, start):
    count += 1

  return count

print("Part 1:", solve(False))
print("Part 2:", solve(True)+1)