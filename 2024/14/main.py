from aoc.common import *

@dataclass
class Robot:
  x: int
  y: int
  dx: int
  dy: int

  def move(self, i):
    self.x = (self.x + self.dx * i) % m
    self.y = (self.y + self.dy * i) % n

def make_robot(line):
  x, y, dx, dy = map(int, re.match(r'p=(\d+),(\d+) v=([-\d]+),([-\d]+)', line).groups())
  return Robot(x, y, dx, dy)

_robots = read_input(
    mapper=make_robot
)

if len(_robots) == 12:
  m = 11
  n = 7
else:
  m = 101
  n = 103

robots = deepcopy(_robots)
tl = []
tr = []
bl = []
br = []
for r in robots:
  r.move(100)

  if r.x < m // 2:
    if r.y < n // 2:
      tl.append(r)
    elif r.y > n // 2:
      bl.append(r)
  elif r.x > m // 2:
    if r.y < n // 2:
      tr.append(r)
    elif r.y > n // 2:
      br.append(r)

print("Part 1:", math.prod(map(len, [tl, tr, bl, br])))

robots = deepcopy(_robots)
seconds = 0
while len(set((r.x, r.y) for r in robots)) != len(robots):
  seconds += 1
  for r in robots:
    r.move(1)

print("Part 2:", seconds)

grid = np.zeros((n, m), dtype=int)
for r in robots:
  grid[r.y, r.x] = 1
print_grid(grid)