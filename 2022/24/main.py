grid = open('input.txt').read().splitlines()

width = len(grid[0]) - 2 
height = len(grid) - 2

start = (0, -1)
target = (width - 1, height)

init_storms = []

for i in range(width):
  for j in range(height):
    v = grid[j+1][i+1]
    if v in ['>', '<', '^', 'v']:
      init_storms.append((v, i, j))

def get_storm_locations(storms):
  storm_locations = {}
  for d, i, j in storms:
    storm_locations[(i, j)] = True

  return storm_locations

def distance(loc, target):
  return abs(target[0] - loc[0]) + abs(target[1] - loc[1])

storms_at_t = {
  0: (init_storms, get_storm_locations(init_storms)),
}

def get_next_storms(storms):
  next_storms = []
  for d, i, j in storms:
    if d == ">":
      next_storms.append((d, (i + 1) % width, j))
    if d == "<":
      next_storms.append((d, (i - 1) % width, j))
    if d == "v":
      next_storms.append((d, i, (j + 1) % height))
    if d == "^":
      next_storms.append((d, i, (j - 1) % height))

  return next_storms

def route(to_visit, target):
  current_t = to_visit[0][1]
  visited = {}

  while to_visit:
    if (to_visit[0][1] != current_t):
      to_visit = sorted(to_visit, key=lambda v: v[0])[:min(len(to_visit), 100)]
    _, t, (x, y) = to_visit.pop(0)
    current_t = t

    if (t, (x, y)) in visited:
      continue
    visited[(t, (x, y))] = True

    if (x, y) == target:
      return t

    storms, storm_locations = storms_at_t[t]
    if t+1 in storms_at_t:
      next_storms, next_storm_locations = storms_at_t[t+1]
    else:
      next_storms = get_next_storms(storms)
      next_storm_locations = get_storm_locations(next_storms)
      storms_at_t[t+1] = (next_storms, next_storm_locations)

    for i, j in [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
      if (i < 0) or (i >= width):
        continue
      if (j > height) or (j < -1):
        continue
      if (j == -1) and (x != 0):
        continue
      if (j == height) and (x != width - 1):
        continue

      if (i, j) not in next_storm_locations:
        to_visit.append((distance((i, j), target), (t + 1), (i, j)))


t1 = route([(distance(start, target), 0, start)], target)
print("Part 1:", t1)
t2 = route([(distance(target, start), t1, target)], start)
t3 = route([(distance(start, target), t2, start)], target)
print("Part 2:", t3)