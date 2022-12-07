left = ['A', 'B', 'C']
right = ['X', 'Y', 'Z']

def choose(round):
  opp, outcome = round.split(' ')
  i = left.index(opp)
  j = right.index(outcome)

  return opp + " " + right[(i + j - 1) % 3]

def score(round):
  opp, you = round.split(' ')
  i = left.index(opp)
  j = right.index(you)

  score = j + 1

  if i == j:
    score += 3
  elif (j - i) % 3 == 1:
    score += 6

  return score

rounds = open('input.txt').read().splitlines()

print("Part 1:", sum([score(round) for round in rounds]))
print("Part 2:", sum([score(choose(round)) for round in rounds]))