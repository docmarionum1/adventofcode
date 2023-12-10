from aoc.common import *
import networkx as nx

lines = read_input()

NORTH = ["|", "L", "J"]
SOUTH = ["|", "7", "F"]
EAST = ["-", "L", "F"]
WEST = ["-", "J", "7"]

h = len(lines)
w = len(lines[0])

G = nx.Graph()
S = None
for i in range(h):
  for j in range(w):
    c = lines[i][j]
    if c in NORTH and i > 0 and lines[i-1][j] in SOUTH + ["S"]: # North
      G.add_edge((i, j), (i-1, j))
    if c in SOUTH and i < (h - 1) and lines[i+1][j] in NORTH + ["S"]: # South
      G.add_edge((i, j), (i+1, j))
    if c in EAST and j < (w - 1) and lines[i][j+1] in WEST + ["S"]: # East
      G.add_edge((i, j), (i, j+1))
    if c in WEST and j > 0 and lines[i][j-1] in EAST + ["S"]: # West
      G.add_edge((i, j), (i, j-1))

    if c == "S":
      S = (i, j)

neighbors = list(G.neighbors(S))
G.remove_node(S)

print("Part 1:", int((len(nx.shortest_path(G, *neighbors)) + 1) / 2))

grid = [[" " for _ in range(w*3)] for _ in range(h*3)]
for (i, j) in nx.shortest_path(G, *neighbors):
  c = lines[i][j]
  if c == "|":
    grid[i*3][j*3+1] = "|"
    grid[i*3+1][j*3+1] = "|"
    grid[i*3+2][j*3+1] = "|"
  if c == "-":
    grid[i*3 + 1][j*3] = "-"
    grid[i*3 + 1][j*3+1] = "-"
    grid[i*3 + 1][j*3+2] = "-"
  if c == "L":
    grid[i*3][j*3+1] = "L"
    grid[i*3+1][j*3+1] = "L"
    grid[i*3+1][j*3+2] = "L"
  if c == "J":
    grid[i*3][j*3+1] = "J"
    grid[i*3+1][j*3+1] = "J"
    grid[i*3+1][j*3] = "J"
  if c == "7":
    grid[i*3+2][j*3+1] = "7"
    grid[i*3+1][j*3+1] = "7"
    grid[i*3+1][j*3] = "7"
  if c == "F":
    grid[i*3+2][j*3+1] = "F"
    grid[i*3+1][j*3+1] = "F"
    grid[i*3+1][j*3+2] = "F"

i = S[0]
j = S[1]
for x in range(3):
  for y in range(3):
    grid[i*3+x][j*3+y] = "S"


grid = np.array(grid)
to_visit = []
to_visit_set = {}

def flood_fill(i, j):
  if grid[i,j] == " ":
    grid[i,j] = "O"

  if (i > 0) and (grid[i-1,j] == " ") and (i-1, j) not in to_visit_set:
    to_visit.append((i-1, j))
  if (j > 0) and (grid[i,j-1] == " ") and (i, j-1) not in to_visit_set:
    to_visit.append((i, j-1))
  if (i < (grid.shape[0] - 1)) and (grid[i+1,j] == " ") and (i+1, j) not in to_visit_set:
    to_visit.append((i+1, j))
  if (j < (grid.shape[1] - 1)) and (grid[i,j+1] == " ")  and (i, j+1) not in to_visit_set:
    to_visit.append((i, j+1))

for i in range(grid.shape[0]):
  to_visit.append((i, 0))
  to_visit.append((i, grid.shape[1] - 1))

while to_visit:
  (i, j) = to_visit.pop()
  flood_fill(i, j)

print("Part 2:", (np.argwhere(grid == " ") % 3 == 1).all(axis=1).sum())