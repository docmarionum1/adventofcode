from aoc.common import *

lines = read_input(mapper=lambda l: split(l, mapper=int))

def next_value(i, sign, a):
  diff = np.diff(a)

  if (diff == diff[0]).all():
    return a[i] + diff[0] * sign

  return a[i] + next_value(i, sign, diff) * sign

print("Part 1:", sum(map(functools.partial(next_value, -1, 1), lines)))
print("Part 2:", sum(map(functools.partial(next_value, 0, -1), lines)))