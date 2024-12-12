from aoc.common import *

grid = np_grid_to_dict(read_grid().astype(int))

trailheads = []
G = nx.DiGraph()
for loc, v in grid.items():
  G.add_node(loc, v=v)
  if v == 0:
    trailheads.append(loc)
  for n in neighbors(*loc):
    if grid.get(n, -1) == v + 1:
      G.add_edge(loc, n)

count = 0
for trailhead in trailheads:
  count += len(nx.descendants_at_distance(G, trailhead, 9))
print("Part 1:", count)

count = 0
for trailhead in trailheads:
  for target in nx.descendants_at_distance(G, trailhead, 9):
    count += len(list(nx.all_simple_paths(G, trailhead, target)))
print("Part 2:", count)