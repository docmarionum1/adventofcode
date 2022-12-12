import numpy as np
grid = np.array(list(map(list, open('input.txt').read().splitlines()))).astype(int)

# Part 1

a = np.maximum.accumulate(grid)
a = np.pad(a, 1, constant_values=-1)[:-2,1:-1]
b = np.maximum.accumulate(grid, axis=1)
b = np.pad(b, 1, constant_values=-1)[1:-1,:-2]
c = np.maximum.accumulate(grid[::-1,:])[::-1,:]
c = np.pad(c, 1, constant_values=-1)[2:,1:-1]
d = np.maximum.accumulate(grid[:,::-1], axis=1)[:,::-1]
d = np.pad(d, 1, constant_values=-1)[1:-1,2:]

print("Part 1:", ((grid > a) | (grid > b) | (grid > c) | (grid > d)).sum())

# Part 2

def countfn(h, i, j, di, dj):
  count = 0
  while (i >= 0) and (i < len(grid)) and (j >= 0) and (j < len(grid)):
    count += 1
    if (grid[j][i] >= h):
      break
    i += di
    j += dj
  return count

def scorefn(x, y):
  score = 1
  h = grid[y][x]

  score *= countfn(h, x - 1, y, -1, 0)
  score *= countfn(h, x + 1, y, 1, 0)
  score *= countfn(h, x, y - 1, 0, -1)
  score *= countfn(h, x, y + 1, 0, 1)

  return score

scores = []
for i in range(len(grid)):
  for j in range(len(grid)):
    s = scorefn(i, j)
    scores.append(s)

print("Part 2:", max(scores))