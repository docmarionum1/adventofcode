from aoc.common import *

inputs, gates = read_input(
    delim="\n\n",
)

inputs = split(inputs, delim="\n", mapper=lambda x: re.match(r"(.*): (.*)", x).groups())
inputs = {k: v == '1' for k, v in inputs}

gates = split(
    gates,
    delim="\n",
    mapper=lambda x: re.match(r"(.*) ([A-Z]{2,3}) (.*) -> (.*)", x).groups()
)

def read_value(p, inputs, return_int=True):
  binary = "".join([
    str(int(inputs[k]))
    for k in
    sorted([k for k in inputs if k[0] == p])[::-1]
  ])

  if return_int:
    return int(binary, 2)
  else:
    return binary

def run(inputs, gates):
  inputs = dict(inputs)
  gates = list(gates)

  while gates:
    a, op, b, c = gates.pop(0)
    if (a not in inputs) or (b not in inputs):
      gates.append((a, op, b, c))
      continue

    if op == "AND":
      inputs[c] = inputs[a] and inputs[b]
    elif op == "OR":
      inputs[c] = inputs[a] or inputs[b]
    elif op == "XOR":
      inputs[c] = inputs[a] != inputs[b]

  return read_value("z", inputs)

print("Part 1:", run(inputs, gates))

G = nx.DiGraph()
for a, op, b, c in gates:
  G.add_node(c, op=op)
  G.add_edge(a, c)
  G.add_edge(b, c)

def test_adder(i):
  i = str(i).zfill(2)
  x = f"x{i}"
  y = f"y{i}"
  z = f"z{i}"

  zp = set(G.predecessors(z))
  xn = set(G.neighbors(x))
  xy_xor = (zp & xn).pop()
  xy_and = (xn - {xy_xor}).pop()
  carry_in = (zp - {xy_xor}).pop()
  carry_and = (
      set(G.neighbors(carry_in)) &
      set(G.neighbors(xy_xor))
      - {z}
  ).pop()
  carry_or = set(G.neighbors(carry_and)).pop()

  invalid = []

  if G.nodes[xy_xor]["op"] != "XOR":
    invalid.append(xy_xor)
  if G.nodes[xy_and]["op"] != "AND":
    invalid.append(xy_and)
  if G.nodes[z]["op"] != "XOR":
    invalid.append(z)
  if G.nodes[carry_and]["op"] != "AND":
    invalid.append(carry_and)
  if G.nodes[carry_or]["op"] != "OR":
    invalid.append(carry_or)

  return invalid

swaps = []

for i in range(1, 45):
  try:
    swaps.extend(test_adder(i))
  except:
    oz = f"z{str(i).zfill(2)}"
    to_visit = [oz]
    visited = []
    while to_visit:
      z = to_visit.pop(0)
      if z in visited:
        continue
      visited.append(z)

      to_visit.extend(G.neighbors(z))
      to_visit.extend(G.predecessors(z))

      G = nx.relabel_nodes(G, {z: oz, oz: z}, copy=True)

      try:
        invalid = test_adder(i)
        if not invalid:
          swaps.extend([oz, z])
          break
      except:
        pass
      finally:
        G = nx.relabel_nodes(G, {z: oz, oz: z}, copy=True)

print("Part 2:", ",".join(sorted(swaps)))

# Visualize the adder
# !pip install pyvis
# from pyvis.network import Network
# from IPython.display import HTML

# G = nx.DiGraph()
# for a, op, b, c in gates:
#   G.add_node(c, op=op)
#   G.add_edge(a, f"{op}_{c}")
#   G.add_edge(b, f"{op}_{c}")
#   G.add_edge(f"{op}_{c}", c)

# net = Network(
#         notebook=True,
#     cdn_resources='in_line'
# )
# net.show_buttons()
# net.from_nx(G)
# net.save_graph("adder.html")
# HTML(filename="adder.html")