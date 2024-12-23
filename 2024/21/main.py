from aoc.common import *

lines = read_input()

numeric_keypad = """789
456
123
.0A"""
numeric_G = read_grid(
    text=numeric_keypad,
    return_type="nx",
    neighbor_data="arrow",
    invalid_char=".",
)
numeric_grid = read_grid(
    text=numeric_keypad,
    return_type="dict"
)
numeric_coords = {v:k for k,v in numeric_grid.items()}

directional_keypad = """.^A
<v>"""
directional_G = read_grid(
    text=directional_keypad,
    return_type="nx",
    neighbor_data="arrow",
    invalid_char=".",
)
directional_grid = read_grid(
    text=directional_keypad,
    return_type="dict"
)
directional_coords = {v:k for k,v in directional_grid.items()}

def path_to_presses(G, path):
  presses = []
  for i in range(len(path)-1):
    presses.append(G.edges[path[i], path[i+1]]['arrow'])

  return "".join(presses) + "A"

def press_len(presses):
  l = 0
  for i in range(len(presses)-1):
    a = directional_coords[presses[i]]
    b = directional_coords[presses[i+1]]
    l += abs(a.real - b.real) + abs(a.imag - b.imag)

  return l

@functools.cache
def all_shortest_paths(G, start, end):
  return list(map(
    functools.partial(path_to_presses, G),
    nx.all_shortest_paths(G, start, end)
  ))

@functools.cache
def shortest_path(G, start, end):
  return sorted(map(
    functools.partial(path_to_presses, G),
    nx.all_shortest_paths(G, start, end)
  ), key=press_len)[0]

@functools.cache
def directional_step(start, end, n):
  start = directional_coords[start]
  end = directional_coords[end]

  paths = all_shortest_paths(directional_G, start, end)
  
  if n == 1:
    return len(paths[0])

  ses = []
  for path in paths:
    s = 0
    loc = "A"
    for i, c in enumerate(path):
      s += directional_step(loc, c, n-1)
      loc = c
    ses.append(s)

  return min(ses)

  return s

def solve(code, n):
  # Directions to operate the numeric keypad
  code = "A" + code
  new_code = "A"
  for i in range(len(code)-1):
    new_code += shortest_path(numeric_G, numeric_coords[code[i]], numeric_coords[code[i+1]])
    
  # Number of directions to operate the directional keypads
  s = 0
  for i in range(len(new_code)-1):
    s += directional_step(new_code[i], new_code[i+1], n)

  return s

def part(n):
  complexity = 0
  for code in lines:
    complexity += solve(code, n) * int(code[:3])
  return complexity

print("Part 1:", part(2))
print("Part 2:", part(25))