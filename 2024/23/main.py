from aoc.common import *

lines = read_input(
    mapper = lambda x: x.split("-")
)

G = nx.Graph()
for a, b in lines:
  G.add_edge(a, b)

t = set(n for n in G.nodes() if n[0] == "t")
count = 0
largest = []
for comp in nx.enumerate_all_cliques(G):
  if (len(comp) == 3) and (t & set(comp)):
    count += 1
  if len(comp) > len(largest):
    largest = comp

print("Part 1:", count)
print("Part 2:", ",".join(sorted(largest)))