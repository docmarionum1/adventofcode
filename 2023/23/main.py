from aoc.common import *

grid = read_grid()
h, w = grid.shape

G = nx.DiGraph()
starting_point = (0, 1)
ending_point = (h-1, w-2)
to_visit = [starting_point]
visited = set()
intersections = set()

while to_visit:
  start = to_visit.pop()
  visited.add(start)
  dist = 0
  i,j = start
  visited_this_path = set()

  while True:
    visited_this_path.add((i,j))
    if grid[i,j] == "^":
      neighbors = [(-1, 0)]
    elif grid[i,j] == "v":
      neighbors = [(1, 0)]
    elif grid[i,j] == "<":
      neighbors = [(0, -1)]
    elif grid[i,j] == ">":
      neighbors = [(0, 1)]
    else:
      neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    actual_neighbors = []

    for dy,dx in neighbors:
      y = i + dy
      x = j + dx
      if y >= 0 and x >= 0 and y < h and x < w and grid[y,x] != "#" and (y,x) not in visited_this_path:
        actual_neighbors.append((y,x))

    if len(actual_neighbors) == 0:
      G.add_edge(start, (i,j), weight=dist)
      break
    elif len(actual_neighbors) == 1:
      i,j = actual_neighbors[0]
      dist += 1
    else:
      G.add_edge(start, (i,j), weight=dist)
      intersections.add((i,j))
      for n in actual_neighbors:
        G.add_edge((i,j), n, weight=1)
      to_visit = to_visit + [n for n in actual_neighbors if n not in visited]
      break


# Compress network
critical_points = set(intersections)
critical_points.add(starting_point)
critical_points.add(ending_point)

to_visit = [[n] for n in critical_points]
G2 = nx.DiGraph()

while to_visit:
  current_path = to_visit.pop()
  if (
      len(current_path) > 1 and 
      current_path[0] in critical_points and 
      current_path[-1] in critical_points
  ):
    G2.add_edge(current_path[0], current_path[-1], weight=nx.path_weight(G, current_path, "weight"))
    continue

  neighbors = G[current_path[-1]]
  to_visit = to_visit + [current_path + [n] for n in neighbors if n not in current_path]

print("Part 1:", max((nx.path_weight(G2, p, "weight")) for p in nx.all_simple_paths(G2, starting_point, ending_point)))
G3 = G2.to_undirected()
print("Part 2:", max((nx.path_weight(G3, p, "weight")) for p in nx.all_simple_paths(G3, starting_point, ending_point)))