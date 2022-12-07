def parse(assignment):
  return [tuple(map(int, elf.split('-'))) for elf in assignment.split(',')]
assignments = list(map(parse, open('input.txt').read().splitlines()))

def part1(a, b):
  return ((a[0] <= b[0]) and (a[1] >= b[1])) or ((b[0] <= a[0]) and (b[1] >= a[1]))

print("Part 1:", sum([part1(*a) for a in assignments]))

def part2(a, b):
  return (
      ((a[0] >= b[0]) and (a[0] <= b[1])) or 
      ((b[0] >= a[0]) and (b[0] <= a[1]))
  )

print("Part 2:", sum([part2(*a) for a in assignments]))