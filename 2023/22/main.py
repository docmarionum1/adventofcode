def parse_line(line):
  return list(map(int, re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line).groups()))

lines = read_input(mapper=parse_line)

w,h,d = np.array(lines).max(axis=0)[3:]
grid = np.zeros((d+1,h+1,w+1))
grid[0] = -1 # Floor

brickq = []
bricks = {}

# Add the bricks to the dict and also queued by the z-index low to high
for i, line in enumerate(lines):
  x1, y1, z1, x2, y2, z2 = line
  label = i+1
  grid[z1:z2+1,y1:y2+1,x1:x2+1] = label
  heapq.heappush(brickq, (z1, label))
  bricks[label] = line

# Move bricks down from bottom to top
def fall(grid, brickq, update_bricks=False):
  settled = []
  fell = set()

  while brickq:
    z1, label = heapq.heappop(brickq)
    x1, y1, z1, x2, y2, z2 = bricks[label]

    # Set the current location to zeros
    grid[z1:z2+1,y1:y2+1,x1:x2+1] = 0

    # While the location underneath is clear shift down
    while grid[z1-1,y1:y2+1,x1:x2+1].sum() == 0:
      fell.add(label)
      z1 -= 1
      z2 -= 1

    grid[z1:z2+1,y1:y2+1,x1:x2+1] = label
    heapq.heappush(settled, (z1, label))
    if update_bricks:
      bricks[label] = (x1, y1, z1, x2, y2, z2)

  return grid, settled, len(fell)

grid, settled, _ = fall(grid, brickq, True)

def part1():
  supported_by = {}
  supports = {}

  # Get mappings of which bricks support and are supported by other bricks
  for label in bricks:
    x1, y1, z1, x2, y2, z2 = bricks[label]
    sb = [l for l in np.unique(grid[z1-1,y1:y2+1,x1:x2+1]) if l not in [0, -1]]
    supported_by[label] = sb
    for l in sb:
      if l not in supports:
        supports[l] = []
      supports[l].append(label)

  # We want to count bricks that are not supporting anything or are supporting
  # only bricks that have other supports
  count = 0
  for label in bricks:
    if label not in supports:
      count += 1
      continue
    blocks_supported = supports[label]
    if all(len(supported_by[l]) > 1 for l in blocks_supported):
      count += 1

  return supports, supported_by, count

supports, supported_by, count = part1()
print("Part 1:", count)

def part2():
  count = 0
  for label in supports: # Only need to consider bricks that support anything
    grid_copy = np.copy(grid)
    x1, y1, z1, x2, y2, z2 = bricks[label]

    # Re-run the fall algorithm with the brick missing
    grid_copy[z1:z2+1,y1:y2+1,x1:x2+1] = 0
    brickq = [b for b in settled if b[0] > z1] # Only consider bricks above
    heapq.heapify(brickq)
    _, _, c = fall(grid_copy, brickq)
    count += c

  return count

# Use supports and supported by to figure out part 2 instead of simulating
def part2_v2(label):
  fell = set([label])
  to_process = [label]

  while to_process:
    label = to_process.pop()
    if label not in supports:
      continue

    for l in supports[label]:
      if set(supported_by[l]).issubset(fell):
        fell.add(l)
        to_process.append(l)

  return len(fell) - 1

print("Part 2:", part2())
print("Part 2 v2:", sum(part2_v2(l) for l in supports))