from aoc.common import *

lines = read_input(mapper=split)

def hand_type(l):
  if l[0] == 5:
    return 7
  if l[0] == 4:
    return 6
  if (l[0] == 3) and (l[1] == 2):
    return 5
  if l[0] == 3:
    return 4
  if (l[0] == 2) and (l[1] == 2):
    return 3
  if (l[0] == 2):
    return 2

  return 1

def sort(part, cards, hand):
  return hand_type(part(hand[0])) * len(cards)**5 + sum([
      len(cards)**i * cards.index(c) for i, c in enumerate(hand[0][::-1])
  ])

def winnings(ranked):
  return sum([
    (i+1) * int(bid) for i, (hand, bid) in enumerate(ranked)
])
  
part1_cards = "23456789TJQKA"
def part1(hand):
  counts = defaultdict(int)

  for card in hand:
    counts[card] += 1

  return sorted(counts.values(), key=lambda c: -c)

part2_cards = "J23456789TQKA"
def part2(hand):
  counts = defaultdict(int)

  jokers = 0

  for card in hand:
    if card == "J":
      jokers += 1
    else:
      counts[card] += 1

  counts = sorted(counts.values(), key=lambda c: -c)

  if jokers == 5:
    return [5]

  counts[0] = counts[0] + jokers

  return counts

print("Part 1:", winnings(sorted(lines, key=functools.partial(sort, part1, part1_cards))))
print("Part 2:", winnings(sorted(lines, key=functools.partial(sort, part2, part2_cards))))