import itertools
import math
import re

with open('../input.txt') as f:
  lines = f.read().splitlines()

def process(expr):
  i = 0
  split_match = None
  depth = 0
  while i < len(expr):
    # Explode
    if depth == 4:
      match = re.match(r'\[\d+\,\d+\]', expr[i:])
      if match:
        left = expr[:i]
        right = expr[i+match.end():]
        pair = eval(match.group())

        # left
        numbers = list(re.finditer(r'\d+', left))
        if numbers:
          lmatch = numbers[-1]
          left = left[:lmatch.start()] + str(int(lmatch.group()) + pair[0]) + left[lmatch.end():]
          
        # right
        numbers = list(re.finditer(r'\d+', right))
        if numbers:
          rmatch = numbers[0]
          right = right[:rmatch.start()] + str(int(rmatch.group()) + pair[1]) + right[rmatch.end():]

        return left + "0" + right

    
    # Match numbers
    match = re.match(r'\d+', expr[i:])
    if match:
      if split_match is None and int(match.group()) > 9:
        # Save split in case we don't find an explode
        split_match = i, match

      i += len(match.group())

      continue

    if expr[i] == "[":
      depth += 1
    if expr[i] == "]":
      depth -= 1

    i += 1

  if split_match:
    i, match = split_match
    left = expr[:i]
    right = expr[i+match.end():]
    num = int(match.group())

    return left + f"[{num//2},{int(math.ceil(num/2))}]" + right


def add(expr):
  while True:
    result = process(expr)
    if result:
      expr = result
    else:
      break

  return expr

def magnitude(expr):
  return (
    3 * (magnitude(expr[0]) if isinstance(expr[0], list) else expr[0]) +
    2 * (magnitude(expr[1]) if isinstance(expr[1], list) else expr[1])
  )

  return result

current = None
for line in lines:
  if current is None:
    current = line
  else:
    current = f"[{current},{line}]"
    current = add(current)

# Part 1
print("Part 1:", magnitude(eval(current)))

# Part 2
max_mag = 0
for a, b in itertools.combinations(lines, 2):
  max_mag = max(max_mag, magnitude(eval(add(f"[{a},{b}]"))))
  max_mag = max(max_mag, magnitude(eval(add(f"[{b},{a}]"))))

print("Part 2:", max_mag)