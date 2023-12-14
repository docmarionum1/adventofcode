from aoc.common import *

lines = read_input()

def count(line, part2=False):
  springs, groups = line.split(' ')

  if part2:
    springs = '?'.join([springs for _ in range(5)])
    groups = ','.join([groups for _ in range(5)])

  groups = tuple(map(int, groups.split(',')))

  memo = {}

  def f(springs, groups):
    if (springs, groups) in memo:
      return memo[(springs, groups)]

    # We've exausted all of the groups and don't have # left
    if not groups and '#' not in springs:
      return 1

    # Otherwise we've exausted them but incorrerctly
    if not groups:
      return 0

    # Impossible case where we have fewer slots left than sum(groups)
    if len(springs) < sum(groups):
      return 0

    # If the first character is a gap, skip it
    if springs[0] == '.':
      n = f(springs[1:], groups)
      memo[(springs, groups)] = n
      return n

    # If the first character is a ?
    if springs[0] == "?":
      # Treat the current spring as "."
      a = f(springs[1:], groups)

      # Treat the current spring as "#"
      b = f("#" + springs[1:], groups)

      memo[(springs, groups)] = a + b
      return a + b

    else:
      # Otherwise the current group must fit in the current run of springs
      group = groups[0]
      current_spring_group = re.split(r'\.+', springs)[0]

      # Current group is too short
      if len(current_spring_group) < group:
        return 0

      # Current group would end up with a # at the end (no space)
      if group < len(springs) and springs[group] == '#':
        return 0

      n = f(springs[group+1:], groups[1:])

      memo[(springs, groups)] = n
      return n

  return f(springs, groups)

print("Part 1:", sum([count(l) for l in lines]))
print("Part 2:", sum([count(l, True) for l in lines]))