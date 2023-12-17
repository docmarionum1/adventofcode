from aoc.common import *

steps = read_input(delim=',')

def hash(s):
  v = 0
  for c in s:
    v = ((v + ord(c)) * 17) % 256

  return v

print("Part 1:", sum(map(hash, steps)))

boxes = [[] for i in range(256)]
def hashmap(s):
  label, op, lens = re.match(r'([a-z]+)([=-])(\d*)', s).groups()
  box = hash(label)

  exists = bool([l for l in boxes[box] if l[0] == label])

  if op == "-":
    if exists:
      boxes[box] = [l for l in boxes[box] if l[0] != label]

  elif op == "=":
    if exists:
      boxes[box] = [(label, lens) if l[0] == label else l for l in boxes[box]]
    else:
      boxes[box] = boxes[box] + [(label, lens)]

list(map(hashmap, steps))
print("Part 2:", sum([(i+1) * sum([(j+1) * int(l[1]) for j,l in enumerate(b)]) for i,b in enumerate(boxes) if b]))