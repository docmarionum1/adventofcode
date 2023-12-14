from aoc.common import *
patterns = read_input(delim='\n\n', mapper=lambda p: read_grid(text=p))

def find_middle(grid, threshold):
  h = len(grid)
  for i in range(1, h):
    j = 1
    reflect = True
    while reflect and (i-j >= 0) and (i+j-1 < h):
      mismatches = (grid[i-j:i] != grid[i+j-1:i-1:-1]).sum()
      if mismatches > threshold:
        reflect = False
      j += 1

    if reflect and mismatches == threshold:
      return i


def summarize(grid, threshold=0):
  r = find_middle(grid, threshold)
  if r:
    return r * 100

  return find_middle(np.transpose(grid), threshold)

print("Part 1:", sum([summarize(p, 0) for p in patterns]))
print("Part 2:", sum([summarize(p, 1) for p in patterns]))