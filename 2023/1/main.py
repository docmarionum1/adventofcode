from aoc.common import *

lines = open('input.txt').read().strip().split('\n')

words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
map = {w: str(i+1) for i,w in enumerate(words)}

def convert(n):
  return map.get(n, n)

def f(l, part2='|'.join(words)):
  return int("".join([
      convert(re.search(f"[1-9]|{part2}", l)[0]),
      convert(re.search(f"[1-9]|{part2[::-1]}", l[::-1])[0][::-1]),
  ]))

print("Part 1:", sum([f(l,"😊") for l in lines]))
print("Part 2:", sum([f(l) for l in lines]))
