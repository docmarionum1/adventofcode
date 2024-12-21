from aoc.common import *

grid = read_grid(return_type="dict")

dirs = ["East", "South", "West", "North"]

start = None
end = None
G = nx.DiGraph()
for cell, value in grid.items():
  if value == "#":
    continue

  for i, (d, n) in enumerate(zip(dirs, neighbors(cell))):

    # Return to cell without direction
    if value == "E":
      G.add_edge((cell, d), cell, cost=0)

    # Rotate either direction
    G.add_edge((cell, d), (cell, dirs[(i+1) % len(dirs)]), cost=1000)
    G.add_edge((cell, d), (cell, dirs[(i-1) % len(dirs)]), cost=1000)

    # Go to neighbor
    if grid.get(n, "#") != "#":
      G.add_edge((cell, d), (n, d), cost=1)

  if value == "S":
    start = (cell, "East")

  if value == "E":
    end = cell

print("Part 1:", nx.shortest_path_length(G, start, end, "cost"))

tiles = set()
for path in nx.all_shortest_paths(G, start, end, "cost"):
  for tile in path:
    if isinstance(tile, tuple):
      tiles.add(tile[0])
    else:
      tiles.add(tile)

print("Part 2:", len(tiles))