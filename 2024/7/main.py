from aoc.common import *

lines = read_input(
    mapper=lambda l: map2(
        split_strip(l, delim=": "),
        int,
        functools.partial(split, mapper=int)
    )
)

def is_correct(result, operands, operators):
  if len(operands) == 1:
    return result == operands[0]

  for op in operators:
    if is_correct(result, [op(operands[:2])] + operands[2:], operators):
      return result

  return 0

correct = 0
incorrect = []
for result, operands in lines:
  if is_correct(result, operands, [sum, math.prod]):
    correct += result
  else:
    incorrect.append((result, operands))

print("Part 1:", correct)

def concat(a):
  return int(str(a[0]) + str(a[1]))

for result, operands in incorrect:
   correct += is_correct(result, operands, [sum, math.prod, concat])

print("Part 2:", correct)