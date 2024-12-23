from aoc.common import *

def mix(secret_number, a):
  return a ^ secret_number

def prune(secret_number):
  return secret_number % 16777216

def evolve(secret_number):
  secret_number = prune(mix(secret_number, secret_number * 64))
  secret_number = prune(mix(secret_number, secret_number // 32))
  secret_number = prune(mix(secret_number, secret_number * 2048))
  return secret_number

sequences = []

def process(n, secret_number):
  sequence = []
  for _ in range(n):
    sequence.append(secret_number % 10)
    secret_number = evolve(secret_number)

  sequence.append(secret_number % 10)
  sequences.append(sequence)

  return secret_number


lines = read_input(
    mapper=int
)

print("Part 1:", sum(map(functools.partial(process, 2000), lines)))

all_bananas = []
unique_sequences = set()
for sequence in sequences:
  diff = np.diff(sequence)
  d = dict()
  for i in range(len(diff)-4):
    t = (diff[i], diff[i+1], diff[i+2], diff[i+3])
    if t not in d:
      d[t] = sequence[i+4]
    unique_sequences.add(t)
  all_bananas.append(d)

m = 0
for s in unique_sequences:
  m = max(m, sum(map(lambda b: b.get(s, 0), all_bananas)))

print("Part 2:", m)