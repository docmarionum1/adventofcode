import functools
import itertools

#lines = [eval(line) for line in open('input.txt').read().splitlines() if line]
# Slightly more concise, but harder to read than the above; 
# filter(None|bool, ...) filters out falsey values from a list
lines = list(map(eval, filter(bool, open('input.txt').read().splitlines())))

def compare(left, right):
  if isinstance(left, list) and isinstance(right, list):
    for (l, r) in itertools.zip_longest(left, right):
      if l == None:
        return -1
      elif r == None:
        return 1
      
      cmp = compare(l, r)
      if cmp != 0:
        return cmp

    return 0
  elif isinstance(right, list):
    return compare([left], right)
  elif isinstance(left, list):
    return compare(left, [right])

  if left < right:
    return -1
  elif left > right:
    return 1
  return 0

print("Part 1:", sum([
  i + 1 for i, pair in enumerate(zip(lines[::2], lines[1::2]))
  if compare(*pair) == -1
]))

sorted_lines = sorted(lines + [[[2]],[[6]]], key=functools.cmp_to_key(compare))
print("Part 2:", (sorted_lines.index([[2]]) + 1) * (sorted_lines.index([[6]]) + 1))