elves = open('input.txt').read().split('\n\n')
elves = [sum([int(c) for c in elf.splitlines()]) for elf in elves]
print("Part 1:", max(elves))
print("Part 2:", sum(sorted(elves)[-3:]))