from pathlib import Path
import numpy as np

path = "../input.txt"
puzzle_input = Path(path).read_text().strip()

dots = []
folds = []
for line in puzzle_input.splitlines():
  if not line.strip():
    continue

  if 'fold' in line:
    axis, coord = line.strip()[11:].split("=")
    folds.append((axis, int(coord)))
  else:
    dots.append([int(p) for p in line.strip().split(',')])

dots = np.array(dots)
paper = np.zeros((dots[:,1].max()+1, dots[:,0].max()+1))

for x,y in dots:
  paper[y,x] = 1

for i, (axis, coord) in enumerate(folds):
  if axis == 'y':
    paper = paper[:coord,:] + paper[-1:coord:-1,:]
  else:
    paper = paper[:,:coord] + paper[:,-1:coord:-1]

  paper = (paper >= 1)

  if i == 0:
    print("Part 1:", paper.sum())

print("Part 2:")
for line in paper:
  print("".join("☺" if i else " " for i in line))