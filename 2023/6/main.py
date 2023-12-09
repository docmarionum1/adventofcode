from aoc.common import *

# Brute Force
def ways_to_win(time, distance):
  ways = 0
  for i in range(time+1):
    if (time - i) * i > distance:
      ways += 1

  return ways

# Solve quadratic
def ways_to_win(time, distance):
  b = -time
  c = distance + 1e-9 # Strictly greater

  # calculate the discriminant
  d = (b**2) - (4*c)

  return (
    math.floor(((-b+cmath.sqrt(d))/2).real) -
    math.ceil(((-b-cmath.sqrt(d))/2).real) + 1
  )

races = zip(*read_input(mapper=lambda l: split(split(l, ':')[1], r'\s+', int)))
print("Part 1:", np.product([ways_to_win(*r) for r in races]))

race = read_input(
    mapper=lambda l: int(''.join(split(split(l, ':')[1], r'\s+')))
)
print("Part 2:", ways_to_win(*race))