from aoc.common import *

grid = read_grid()

w, h = grid.shape
start = tuple(np.argwhere(grid == "S")[0])

# Get the shortest distance between the start and each point on the grid
to_visit = [(0, start)]
visited = set()

dists = np.ones(grid.shape) * 1000

while to_visit:
  d, (i, j) = heapq.heappop(to_visit)
  if (i,j) in visited:
    continue
  dists[i,j] = d
  visited.add((i, j))

  for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    x = j + dx
    y = i + dy
    if x >= 0 and y >= 0 and x < w and y < h and (y,x) not in visited:
      if grid[y,x] != '#':
        heapq.heappush(to_visit, (d+1, (y,x)))

# Part 1 is the even parity squares that are less than 65 steps away (the inner diamond)
print("Part 1:", ((dists < 65) & (dists % 2 == 0)).sum())

# Part 2
# Cribbed ;_; from
# https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
even_corners = ((dists < 1000) & (dists % 2 == 0) & (dists > 65)).sum()
odd_corners = ((dists < 1000) & (dists % 2 == 1) & (dists > 65)).sum()

even_full = ((dists < 1000) & (dists % 2 == 0)).sum()
odd_full = ((dists < 1000) & (dists % 2 == 1)).sum()

steps = 26501365
n = (steps - ((w - 1)/2)) / w

print("Part 2:", int(n**2 * even_full + (n+1)**2 * odd_full - (n+1) * odd_corners + n*even_corners))