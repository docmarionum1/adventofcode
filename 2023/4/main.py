from aoc.common import *

def get_cards(line):
  return tuple(map(
      lambda g: split_strip(g, mapper=int, delim=r"\s+"),
      re.match(r'Card\s+\d+: ([0-9 ]*) \| ([0-9 ]*)', line).groups()
  ))

cards = read_input(mapper=get_cards)

def part1(winning, mine):
  n = len(set(winning).intersection(mine))
  return 2 ** (n - 1) if n else 0

def part2(cards):
  copies = {i: 1 for i in range(len(cards))}

  for i, (winning, mine) in enumerate(cards):
    matches = len(set(winning).intersection(mine))
    for j in range(i+1, i+matches+1):
      copies[j] += copies[i]

  return sum(copies.values())

print("Part 1:", sum([part1(*c) for c in cards]))
print("Part 2:", part2(cards))
