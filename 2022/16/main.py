from heapq import heappop, heappush
import re

nodes = open('input.txt').read().splitlines()
nodes = [re.match('.*([A-Z]{2}) has flow rate=(\d+); [a-z ]*([A-Z ,]+)', n).groups() for n in nodes]

class Node:
  def __init__(self, name, flow_rate, neighbors):
    self.flow_rate = flow_rate
    self.name = name
    self.neighbors = neighbors

  def preassure_released(self, time_remaining):
    return self.flow_rate * time_remaining

  def distance_to_key_nodes(self, opened):
    return [
      (other, shortest_paths[(self.name, other)]) 
      for other in key_nodes
      if (self.name != other) and (other not in opened)
    ]

graph = {}

for node, flow_rate, neighbors in nodes:
  graph[node] = Node(node, 0, neighbors.split(", "))
  if int(flow_rate) > 0:
    graph[node].neighbors += [node + "_open"]
    graph[node + "_open"] = Node(node + "_open", int(flow_rate), neighbors.split(", "))

shortest_paths = {}

# Start, current, length
to_visit = [(n.name, n.name, 0) for n in graph.values()]
visited = set()

while to_visit:
  state = to_visit.pop()
  visited.add(state)
  start, curr, length = state
  if (start, curr) not in shortest_paths or length < shortest_paths[(start, curr)]:
    shortest_paths[(start, curr)] = length

  for neighbor in graph[curr].neighbors:
    if (start, neighbor) not in visited:
      if (start, neighbor) not in shortest_paths or (length + 1) < shortest_paths[(start, neighbor)]:
        to_visit.append((start, neighbor, length + 1))

key_nodes = sorted([n for n in graph if "_open" in n], key=lambda n: -graph[n].flow_rate)

def solve(states, heuristic):
  visited = set()
  max_max_preassure = 0

  while states:
    preassure, ynn, yt, enn, et, opened = heappop(states)
    if preassure < max_max_preassure:
      max_max_preassure = preassure

    if yt <= 1 and et <= 1:
      continue

    if yt:
      y_neighbors = graph[ynn].distance_to_key_nodes(opened)
    else:
      y_neighbors = [(None, 0)]

    if et:
      e_neighbors = graph[enn].distance_to_key_nodes(opened)
    else:
      e_neighbors = [(None, 0)]

    for nynn, yd in y_neighbors:
      for nenn, ed in e_neighbors:
        if nynn == nenn:
          continue
        if (nynn in opened) or (nenn in opened):
          continue

        new_opened = list(opened)

        ytr = max(yt - yd, 0)
        if ytr == 0:
          nynn = "None" # stay put
        else:
          new_opened.append(nynn)

        etr = max(et - ed, 0)
        if etr == 0:
          nenn = "None" # stay put
        else:
          new_opened.append(nenn)

        new_preassure = (
          preassure - 
          (graph[nynn].preassure_released(ytr) if ytr else 0) - 
          (graph[nenn].preassure_released(etr) if etr else 0)
        )

        if new_preassure < (max_max_preassure + (heuristic * (ytr + etr))):
          new_state = (
              new_preassure,
              nynn, ytr, nenn, etr, tuple(new_opened)
          )
          if new_state not in visited:
            heappush(states, new_state)
            visited.add(new_state)

  return -1*max_max_preassure

print("Part 1:", solve([(0, "AA", 30, "AA", 0, tuple())], 50))
print("Part 2:", solve([(0, "AA", 26, "AA", 26, tuple())], 40))