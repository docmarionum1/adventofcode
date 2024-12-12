from aoc.common import *

grid = np_grid_to_dict(read_grid())

def area(r):
  return len(r)

def fences(j, i):
  # Slightly offset neighbors to handle vertical and horizontal offsets.
  # I.e. A fence above (2, 0) and a fence below (0, 0) are not the same.
  return [(j+1.1, i), (j-.2, i), (j, i+1.1), (j, i-.2)]

def add_side(sides, m):
  for s in sides: # Each existing side
    for f in s: # Each fence in that side
      if m in neighbors(*f): # If m is a neighbor
        s.append(m)
        return
  sides.append([m])

def perimeter(r):
  sides = []
  for cell in sorted(r):
    for n, m in zip(neighbors(*cell), fences(*cell)):
      if n not in r:
        add_side(sides, m)

  # return (num sides, num individual fences)
  return sum(len(s) for s in sides), len(sides)

visited = set()
def flood_fill(n: tuple[int, int]):
  if n in visited:
    return []

  visited.add(n)
  plant = grid[n]
  region = set()  
  queue = [n]

  while queue:
    n = queue.pop()
    region.add(n)
    visited.add(n)
    for m in neighbors(*n):
      if m not in region and grid.get(m, None) == plant:
        queue.append(m)

  return region

part1 = 0
part2 = 0
for n in grid.keys():
  r = flood_fill(n)
  a = area(r)
  p1, p2 = perimeter(r)

  part1 += a * p1
  part2 += a * p2

print("Part 1:", part1)
print("Part 2:", part2)