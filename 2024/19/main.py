from aoc.common import *

patterns, towels = read_input(
    delim="\n\n",
)

patterns = split(patterns, delim=", ")
towels = read_input(text=towels)

@functools.cache
def num_ways(towel):
  if towel == "":
    return 1

  s = 0
  for p in patterns:
    if towel.startswith(p):
      s += num_ways(towel.removeprefix(p))

  return s

print("Part 1:", sum(map(bool, map(num_ways, towels))))
print("Part 2:", sum(map(num_ways, towels)))