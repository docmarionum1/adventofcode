from aoc.common import *

cutoff = 100

grid = read_grid(return_type="dict")

start = [k for k, v in grid.items() if v == "S"][0]
end = [k for k, v in grid.items() if v == "E"][0]

# Construct the graph without cheating
G = nx.DiGraph()
for cell, value in grid.items():
  if value == "#":
    continue

  for n in neighbors(cell):
    if grid.get(n, "#") != "#":
      G.add_edge(cell, n, cost=1)

# Cache the distance from each cell to the end
dist_to_end = {}
for source, path in nx.shortest_path(G, target=end).items():
  dist_to_end[source] = len(path) - 1
  #H.add_edge((source, False), (end, False), cost=len(path) - 1)

len_without_cheat = nx.shortest_path_length(G, start, end)
max_len = len_without_cheat - cutoff

def solve(cheat_len):
  # Iterate through each path from the start
  count = 0
  for target, path in nx.shortest_path(G, source=start, weight="cost").items():
    len_to_target = len(path) - 1

    if len_to_target >= max_len:
      break

    # Continue if the current len plus the manhattan distance to the end is too
    # big since we know we can't make it
    manhattan_distance = abs(target.real - end.real) + abs(target.imag - end.imag)
    if (len_to_target + manhattan_distance) > max_len:
      continue

    # Adjust the cheat_len down to take into account the max amount of moves
    # remaining
    cheat_len = min(cheat_len, int(max_len - len_to_target))

    # Cheats!
    for j in range(-cheat_len, cheat_len+1):
      for i in range(-cheat_len, cheat_len+1):
        if (abs(j) + abs(i)) <= cheat_len:
          n = target + complex(j, i)
          if (grid.get(n, "#") != "#") and (n != target):
            total_len = len_to_target + dist_to_end[n] + abs(j) + abs(i) - 1
            if total_len < max_len:
              count += 1

  return count

print("Part 1:", solve(2))
print("Part 2:", solve(20))