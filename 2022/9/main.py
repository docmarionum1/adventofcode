import numpy as np

move_map = np.array([["L", None, "R"], ["D", None, "U"]])

def dist(a, b):
  return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def update_knot(a, b):
  if dist(a, b) > 1:
    b[0] += (a[0] - b[0]) / abs(a[0] - b[0]) if (a[0] - b[0]) else 0
    b[1] += (a[1] - b[1]) / abs(a[1] - b[1]) if (a[1] - b[1]) else 0

def solve(n):
  rope = [[0, 0] for _ in range(n)]
  h = rope[0]
  visited = set()

  for step in steps:
    direction, n = step.split(" ")
    n = int(n)
    for _ in range(n):
      idx, move = np.where(move_map == direction)
      h[idx[0]] += (move[0] - 1)

      for i in range(1, len(rope)):
        update_knot(rope[i - 1], rope[i])

      visited.add(tuple(rope[-1]))

  return len(visited)

steps = open('input.txt').read().splitlines()
print("Part 1:", solve(2))
print("Part 2:", solve(10))