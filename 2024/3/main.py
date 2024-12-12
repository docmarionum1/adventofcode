from aoc.common import *

text = open('input.txt').read()

groups = re.findall(r"(?:(mul)\((\d{1,3}),(\d{1,3})\))|((?:don't)|(?:do))\(\)", text)

print("Part 1:", sum(int(g[1]) * int(g[2]) for g in groups if g[0] == "mul"))

enabled = True
s = 0
for g in groups:
  if g[-1] == "don't":
    enabled = False
  elif g[-1] == "do":
    enabled = True
  elif g[0] == "mul":
    if enabled:
      s += int(g[1]) * int(g[2])

print("Part 2:", s)