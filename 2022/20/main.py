class Number:
  def __init__(self, n, k):
    self.n = int(n) * k

def solve(n, k):
  numbers = open('input.txt').read().splitlines()
  numbers = [Number(num, k) for num in numbers]
  order = list(numbers)

  for _ in range(n):
    for o in order:
      idx = numbers.index(o)
      numbers.pop(idx)
      numbers.insert((idx + o.n) % len(numbers), o)

  zero = [num for num in numbers if num.n == 0][0]
  idx = numbers.index(zero)
  return sum([numbers[(idx + m) % len(numbers)].n for m in range(1000, 4000, 1000)])

print("Part 1:", solve(1, 1))
print("Part 2:", solve(10, 811589153))