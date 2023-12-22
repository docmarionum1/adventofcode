from aoc.common import *

import shapely

lines = read_input()

direction_dict = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

def solve(parse_line):
  i,j = 0,0
  verticies = [(i,j)]
  border_meters = 0

  for line in lines:
    direction, meters, hex = re.match(r'([RDLU]) (\d+) \(#([0-9a-f]{6})\)', line).groups()
    direction, meters = parse_line(direction, meters, hex)

    if direction == 'R':
      j = j + meters
    if direction == 'L':
      j = j - meters
    if direction == 'D':
      i = i + meters
    if direction == 'U':
      i = i - meters

    verticies.append((i,j))
    border_meters += meters

  # Use shapely for area, but we could also easily implement it
  # https://stackoverflow.com/a/451482
  return int(shapely.Polygon([(j,i) for (i,j) in verticies]).area + border_meters/2 + 1)

print("Part 1:", solve(lambda direction, meters, hex: (direction, int(meters))))
print("Part 2:", solve(lambda direction, meters, hex: (direction_dict[hex[-1]], int(hex[:5], 16))))