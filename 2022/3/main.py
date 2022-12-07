def priority(item):
  if item > 'Z':
    return ord(item) - ord('a') + 1
  return ord(item) - ord('A') + 27

def part1(rucksack):
  n = int(len(rucksack) / 2)
  return priority(set(rucksack[:n]).intersection(rucksack[n:]).pop())

def part2(a, b, c):
  return priority(set(a).intersection(b).intersection(c).pop())

rucksacks = open('input.txt').read().splitlines()
print("Part 1:", sum([part1(r) for r in rucksacks]))
print("Part 2:", sum([part2(*rucksacks[i:i+3]) for i in range(0, len(rucksacks), 3)]))