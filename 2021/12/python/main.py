import pathlib

def twice(visited):
  for k, v in visited.items():
    if k.islower() and v > 1:
      return True

  return False

def search(node, visited, part2=False):
  if node not in visited:
    visited[node] = 1
  else:
    visited[node] += 1

  if node == "end":
    return [["end"]]

  paths = []

  for connection in cave[node]:
    if connection == "start":
      continue
    if connection not in visited or connection.isupper() or (part2 and not twice(visited)):
      result = search(connection, visited.copy(), part2)
      if result:
        paths += [
          [node] + path for path in result
        ]

  return paths
        

cave = {}
path = "../input.txt"
puzzle_input = pathlib.Path(path).read_text().strip()

for line in puzzle_input.splitlines():
  a, b = line.strip().split("-")

  if a not in cave:
    cave[a] = set()
  if b not in cave:
    cave[b] = set()

  cave[a].add(b)
  cave[b].add(a)

paths = search("start", {"start": 0})
print("Part 1:", len(paths))

paths = search("start", {"start": 0}, True)
print("Part 2:", len(paths))