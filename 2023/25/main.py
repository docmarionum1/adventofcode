from aoc.common import *

lines = read_input()

G = nx.Graph()

for line in lines:
  a, b = split(line, ':')
  for c in split(b):
    G.add_edge(a, c)

for a, b in itertools.combinations(G.nodes, 2):
  edges = nx.minimum_edge_cut(G, a, b)

  if len(edges) == 3:
    break

for a,b in edges:
  G.remove_edge(a, b)

a, b = list(nx.connected_components(G))

print("Part 1:", len(a) * len(b))