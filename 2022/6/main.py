# First Solution

buffer = open('input.txt').read().strip()

def solve(n):
  for i in range(n, len(buffer)):
    if len(set(buffer[i-n:i])) == n:
      return i

print("Part 1:", solve(4))
print("Part 2:", solve(14))

# Linear Solution

buffer = open('input.txt').read().strip()

def solve(n):
  start_i = 0
  letter_to_idx = {buffer[0]: 0}

  for i in range(1, len(buffer)):
    curr = buffer[i]
    if (curr not in letter_to_idx) or (letter_to_idx[curr] < start_i):
      if (i - start_i) == (n - 1):
        return i + 1
    else:
      start_i = letter_to_idx[curr]+1

    letter_to_idx[curr] = i

print("Part 1:", solve(4))
print("Part 2:", solve(14))