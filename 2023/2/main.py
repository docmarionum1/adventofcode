from aoc.common import *

def mapper(line):
  return map2(
    split_strip(line, ":"), 
    lambda gid: int(split_strip(gid)[1]),
    lambda sets: [
      [map2(split_strip(c), int) for c in split_strip(s, ",")]
      for s in split_strip(sets, ";")
    ]
  )

lines = read_input(mapper=mapper)

color_max = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def part1(game_id, sets):
  for s in sets:
    for count, color in s:
      if count > color_max.get(color, count - 1) :
        return 0

  return game_id

print("Part 1:", sum([part1(*l) for l in lines]))

def part2(game_id, sets):
  min_cubes = {
      "red": 0,
      "green": 0,
      "blue": 0,
  }

  for s in sets:
    for count, color in s:
      min_cubes[color] = max(min_cubes[color], count)

  return np.prod(list(min_cubes.values()))

print("Part 2:", sum([part2(*l) for l in lines]))