from aoc.common import *

lines = read_input()

word = "XMAS"

directions = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, -1), (0, -2), (0, -3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (-1, 0), (-2, 0), (-3, 0)],
    [(0, 0), (1, 1), (2, 2), (3, 3)],
    [(0, 0), (-1, -1), (-2, -2), (-3, -3)],
    [(0, 0), (1, -1), (2, -2), (3, -3)],
    [(0, 0), (-1, 1), (-2, 2), (-3, 3)],
]

count = 0

for j in range(len(lines)):
  for i in range(len(lines[0])):
    for dirs in directions:
      match_all = True
      for letter, offset in zip(word, dirs):
        x = i + offset[0]
        y = j + offset[1]
        if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
          match_all = False
          break

        if lines[y][x] != letter:
          match_all = False
          break

      if match_all:
        count += 1

print("Part 1:", count)

count = 0
for j in range(len(lines)):
  for i in range(len(lines[0])):
    if lines[j][i] != "A":
      continue

    valid = True
    a = (i - 1, j - 1)
    b = (i + 1, j + 1)
    c = (i + 1, j - 1)
    d = (i - 1, j + 1)

    for cells in [a, b, c, d]:
      if cells[0] < 0 or cells[1] < 0 or cells[0] >= len(lines[0]) or cells[1] >= len(lines):
        valid = False

    if not valid:
      continue

    if (
        ((lines[a[1]][a[0]] == "M") and (lines[b[1]][b[0]] == "S")) or
        ((lines[a[1]][a[0]] == "S") and (lines[b[1]][b[0]] == "M"))
       ) and (
        ((lines[c[1]][c[0]] == "M") and (lines[d[1]][d[0]] == "S")) or
        ((lines[c[1]][c[0]] == "S") and (lines[d[1]][d[0]] == "M"))
       ):
       count += 1

print("Part 2:", count)