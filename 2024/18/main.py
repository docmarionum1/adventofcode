from aoc.common import *

W = 71
N = 1024
source = complex(0,0)
target = complex(W-1, W-1)

bites = read_input(
    mapper=lambda l: tuple(map(int, l.split(",")))
)

G = make_nx_grid(W, W)
last_shortest_path = None

for i, b in enumerate(bites):
  node = complex(*b[::-1])
  G.remove_node(node)
  if i >= N:
    if not last_shortest_path or node in last_shortest_path:
      try:
        last_shortest_path = nx.shortest_path(G, source, target)
      except:
        print("Part 2:",  ",".join(map(str, b)))
        break

    if i == N:
      print("Part 1:", len(last_shortest_path) - 1)