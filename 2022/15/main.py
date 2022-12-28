import re

target, max_loc, lines = 2000000, 4000000, open('input.txt').read().splitlines()

lines = [tuple(map(int, re.match(r'Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)', line).groups())) for line in lines]

def get_no_beacon_range_on_line(target):
  ranges = []

  for sx, sy, bx, by in lines:
    distance = abs(sx-bx) + abs(sy-by)
    width_on_target = distance - abs(target - sy)
    if width_on_target > 0:
      range_on_target = (sx - width_on_target, sx + width_on_target)
      ranges.append(range_on_target)

  ranges = sorted(ranges, key=lambda r: r[0])

  i = 0
  while i < (len(ranges) - 1):
    j = 0
    a = ranges[i]
    b = ranges[i+1]

    if a[1] >= (b[0] - 1):
      c = (a[0], max(a[1], b[1]))
      ranges[i] = c
      del ranges[i+1]
    else:
      i += 1

  return ranges

print("Part 1:", sum([r[1] - r[0] for r in get_no_beacon_range_on_line(target)]))

def get_beacon_pos(max_loc):
  for t in range(max_loc):
    r = get_no_beacon_range_on_line(t)
    if len(r) > 1:
      return r[0][1] + 1, t
    # Edge case where the beacon is on the edge
    # Not necessary for my input and slows it down
    # if r[0][0] > 0:
    #   return r[0]-1, t
    # elif r[-1][1] < 20:
    #   print(r[1], t)

x, y = get_beacon_pos(max_loc)
print("Part 2:", 4000000 * x + y)