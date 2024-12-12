from aoc.common import *
from dataclasses import dataclass

text = read_input()[0]

@dataclass
class File:
  id: int
  size: int
  start: int

  def checksum(self):
    return (self.id * np.arange(self.start, self.start + self.size)).sum()

def build_disk(text):
  files = []
  gaps = []
  pointer = 0
  id = 0

  for i, block in enumerate(text):
    block = int(block)
    if i % 2 == 0:
      files.append(File(id, block, pointer))
      pointer += block
      id += 1
    else:
      gaps.append(File(None, block, pointer))
      pointer += block

  return files, gaps

# Part 1
files, gaps = build_disk(text)

new_files = []
for f in files[::-1]:
  while f.size:
    if not gaps:
      new_files.append(f)
      break

    gap = gaps.pop(0)

    if gap.start > f.start:
      new_files.append(f)
      gaps.insert(0, gap)
      break
    if gap.size == f.size:
      f.start = gap.start
      new_files.append(f)
      break
    elif gap.size > f.size:
      f.start = gap.start
      new_files.append(f)
      gap.size -= f.size
      gap.start += f.size
      gaps.insert(0, gap)
      break
    else: # gap.size < f.size
      new_files.append(File(f.id, gap.size, gap.start))
      f.size -= gap.size

print("Part 1:", sum([f.checksum() for f in new_files]))

# Part 2
files, gaps = build_disk(text)
gaps_dict = defaultdict(list)
for gap in gaps:
  gaps_dict[gap.size].append((gap.start, gap))

for gaps in gaps_dict.values():
  heapq.heapify(gaps)

for f in files[::-1]:
  first_gap = None
  for size in range(f.size, 10):
    gaps = gaps_dict.get(size, [])
    if gaps and gaps[0][1].start < f.start:
      if not first_gap or (first_gap.start > gaps[0][1].start):
        first_gap = gaps[0][1]

  if first_gap:
    _, gap = heapq.heappop(gaps_dict[first_gap.size])

    f.start = gap.start
    gap.size -= f.size
    gap.start += f.size

    if gap.size:
      heapq.heappush(gaps_dict[gap.size], (gap.start, gap))

print("Part 2:", sum([f.checksum() for f in files]))