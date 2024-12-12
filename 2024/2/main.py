from aoc.common import *

lines = read_input(
    mapper=functools.partial(split_strip, delim=" ", mapper=int)
)

def is_safe(line):
  line = np.array(line)
  diffs = np.diff(line)

  # Check all increasing or decreasing
  signs = np.sign(diffs)
  matching = np.all(signs == -1) | np.all(signs == 1)

  # Check 1-3
  abs_diffs = np.abs(diffs)
  in_range = np.all((abs_diffs >= 1) & (abs_diffs <= 3))

  return matching & in_range

# Part 1
count = 0
for line in lines:
  if is_safe(line):
    count += 1

print("Part 1:", count)

# Part 2
count = 0
for line in lines:
  if is_safe(line):
    count += 1
    continue

  for i in range(len(line)):
    if is_safe(line[:i] + line[i+1:]):
      count += 1
      break

print("Part 2:", count)