from aoc.common import *

lines = read_input()

height = len(lines) - 1
width = len(lines[0]) - 1

sum = 0
gears = defaultdict(list)

def check(number, y, x1, x2):
  valid = False
  for i in range(max(0, x1-1), min(width, x2+1)):
    for j in range(max(0, y-1), min(height, y+2)):
      char = lines[j][i]
      if (char not in string.digits) and char != '.':
        valid = True
        
        if char == "*":
          gears[(j, i)].append(number)

  return valid

for j, line in enumerate(lines):
  for group in re.finditer("\d+", line):
    number = int(group.group(0))
    
    if check(number, j, *group.span()):
      sum += number

print("Part 1:", sum)
print("Part 2:", np.sum([g[0] * g[1] for g in gears.values() if len(g) == 2]))