from aoc.common import *

lines = read_input(
    mapper=functools.partial(split_strip, delim="   ", mapper=int)
)

lines = np.array(lines)
a = np.array(sorted(lines[:,0]))
b = np.array(sorted(lines[:,1]))

print("Part 1:", np.abs(a - b).sum())

s = 0
for i in a:
  s += i * (b == i).sum()

print("Part 2:", s)