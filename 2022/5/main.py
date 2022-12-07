import re

rows = open('input.txt').read().splitlines()
n = [i for i, r in enumerate(rows) if not r][0]
crates, moves = rows[:n-1], rows[n+1:]

def make_stacks():
  stacks = [[] for _ in range(10)]
  for row in crates[::-1]:
    for i, c in enumerate(row[1::4]):
      if c != ' ':
        stacks[i+1].append(c)
  return stacks

def solve(movefn):
  stacks = make_stacks()
  for move in moves:
    n, f, t = map(int, re.match(r'move (\d+) from (\d+) to (\d+)', move).groups())
    movefn(stacks, n, f, t)

  return ''.join(stack[-1] for stack in stacks if stack)

def part1(stacks, n, f, t):
  for i in range(n):
    stacks[t].append(stacks[f].pop())

def part2(stacks, n, f, t):
  stacks[t] += stacks[f][-n:]
  stacks[f] = stacks[f][:-n]

print("Part 1:", solve(part1))
print("Part 2:", solve(part2))