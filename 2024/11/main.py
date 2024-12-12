from aoc.common import *

text = """5 89749 6061 43 867 1965860 0 206250"""

stones = split(text, mapper=int)

def apply(stone):
  if stone == 0:
    return [1]

  str_stone = str(stone)
  if len(str_stone) % 2 == 0:
    return [
        int(str_stone[:len(str_stone)//2]),
        int(str_stone[len(str_stone)//2:])
    ]

  return [stone * 2024]

memo = {}
def blink(stone, blinks):
  if (stone, blinks) in memo:
    return memo[(stone, blinks)]

  if blinks == 0:
    return 1

  stones = apply(stone)
  num_stones = sum([blink(s, blinks-1) for s in stones])
  memo[(stone, blinks)] = num_stones
  return num_stones

print("Part 1:", sum([blink(stone, 25) for stone in stones]))
print("Part 2:", sum([blink(stone, 75) for stone in stones]))