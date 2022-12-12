import networkx as nx

grid = open("input.txt").read().splitlines()
grid = map(str.strip, grid)
grid = list(map(list, grid))

start = None
end = None
G = nx.DiGraph()

def get_value(i, j):
  global start, end

  value = grid[j][i]
  if value == "S":
    start = (i, j)
    value = "a"
  elif value == "E":
    end = (i, j)
    value = "z"

  return value

def attach_neighbors(i, j):
  curr = get_value(i, j)  
  for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
    if (ni >= 0) and (ni < len(grid[0])) and (nj >= 0) and (nj < len(grid)):
      neighbor = get_value(ni, nj)
      if ord(neighbor) <= (ord(curr) + 1):
        G.add_edge((i, j), (ni, nj))

for j in range(len(grid)):
  for i in range(len(grid[j])):
    attach_neighbors(i, j)

print("Part 1:", nx.shortest_path_length(G, start, end))
print("Part 2:", min([
  l for ((i, j), l) in nx.shortest_path_length(G, target=end).items() if grid[j][i] in ['a', 'S']
]))