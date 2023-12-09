from aoc.common import *

lines = read_input()

instructions = lines[0]

nodes = {}
for l in lines[2:]:
  n, l, r = re.match(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)', l).groups()
  nodes[n] = {"L": l, "R": r}

def solve(n, not_solved):
  i = 0

  while not_solved(n):
    n = nodes[n][instructions[i % len(instructions)]]
    i += 1

  return i

# Part 1
print("Part 1:", solve("AAA", lambda n: n != "ZZZ"))


# Implementation of lcm for fun, but we could just use math.lcm
def gcd(a, b):
  a,b = sorted([a, b])
  if a == 0:
    return b

  return gcd(a, b % a)

def lcm(a, b):
  return int(a * (b / gcd(a, b)))

# Part 2
i = [solve(n, lambda n: n[-1] != "Z") for n in nodes if n[-1] == "A"]
print("Part 2:", functools.reduce(lcm, i))