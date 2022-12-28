import re

inp = open('input.txt').read().splitlines()

map, path = inp[:-2], inp[-1]
map_height = len(map)
map_width = max(len(r) for r in map)
map = [r.ljust(map_width, ' ') for r in map]

order = ['R', 'D', 'L', 'U']
dx_dy = {
  'R': (1, 0),
  'D': (0, 1),
  'L': (-1, 0),
  'U': (0, -1),
}

def part1(x, y, d):
  dx, dy = dx_dy[d]
  i, j = (x + dx) % len(map[0]), (y + dy) % len(map)

  while map[j][i] == ' ':
    i = (i + dx) % map_width
    j = (j + dy) % map_height

  return i, j, d, map[j][i]

def follow_path(get_neighbor):
  x, y, d = map[0].index('.'), 0, 'R'

  for step in re.split(r'(L|R)', path):
    if step == 'R':
      d = order[(order.index(d) + 1) % len(order)]
    elif step == 'L':
      d = order[(order.index(d) - 1) % len(order)]
    else:
      for _ in range(int(step)):
        i, j, nd, t = get_neighbor(x, y, d)
        if t == '.':
          x, y, d = i, j, nd
        else:
          break

  return (x+1)*4 + (y+1)*1000 + order.index(d)

print("Part 1:", follow_path(part1))

# Hand computed face locations and transitions for my input
WIDTH = 50
faces = [
  #(x1, y1)
  (50, 0),
  (100, 0),
  (50, 50),
  (0, 100),
  (50, 100),
  (0, 150)
]

transitions = [
  { #0
    # Current direction -> (new face, side of the face, inverted)
    'U': (5, 'L', 1),
    'L': (3, 'L', -1),
  },
  { #1
    'U': (5, 'D', 1),
    'R': (4, 'R', -1),
    'D': (2, 'R', 1),
  },
  { #2
    'L': (3, 'U', 1),
    'R': (1, 'D', 1),
  },
  { #3
    'U': (2, 'L', 1),
    'L': (0, 'L', -1),
  },
  { #4
    'R': (1, 'R', -1),
    'D': (5, 'R', 1),
  },
  { #5
    'R': (4, 'D', 1),
    'D': (1, 'U', 1),
    'L': (0, 'U', 1)
  }
]

def part2(x, y, d):
  dx, dy = dx_dy[d]

  current_face = [fi for fi, (x1, y1) in enumerate(faces) if (x1 <= x < x1 + WIDTH) and (y1 <= y < y1 + WIDTH)][0]
  face_transitions = transitions[current_face]

  # Relative positions on the face
  rx, ry = x - faces[current_face][0], y - faces[current_face][1]

  # We're still on the current face or it's a simple transition
  if ((0 <= rx + dx < WIDTH) and (0 <= ry + dy < WIDTH)) or (d not in face_transitions):
    i, j = (x + dx) % len(map[0]), (y + dy) % len(map)
    return i, j, d, map[j][i]

  new_face, new_side, invert = face_transitions[d]
  nfx, nfy = faces[new_face]

  # The fixed coordinate is the one that tells us where on the new face/side we land
  if dx != 0:
    n = ry
  else:
    n = rx

  if invert == -1:
    if new_side == 'R':
      i = nfx + WIDTH - 1
      j = nfy + WIDTH - n - 1
      nd = 'L'
    elif new_side == 'L':
      i = nfx
      j = nfy + WIDTH - n - 1
      nd = 'R'
    elif new_side == 'U':
      j = nfy
      i = nfx + WIDTH - n - 1
      nd = 'D'
    elif new_side == 'D':
      j = nfy + WIDTH - 1
      i = nfx + WIDTH - n - 1
      nd = 'U'
  else:
    if new_side == 'R':
      i = nfx + WIDTH - 1
      j = nfy + n
      nd = 'L'
    elif new_side == 'L':
      i = nfx
      j = nfy + n
      nd = 'R'
    elif new_side == 'U':
      j = nfy
      i = nfx + n
      nd = 'D'
    elif new_side == 'D':
      j = nfy + WIDTH - 1
      i = nfx + n
      nd = 'U'

  return i, j, nd, map[j][i]

print("Part 2:", follow_path(part2))