from aoc.common import *

lines = read_input()
seeds = split_strip(lines[0][6:], mapper=int)
maps = defaultdict(lambda: defaultdict(dict))

# Parse all of the mappings
i = 2
while i < len(lines):
  m = tuple(re.match(r'(.*)-to-(.*) map:', lines[i]).groups())
  i += 1

  rows = []
  while i < len(lines) and lines[i]:
    rows.append(list(split(lines[i], mapper=int)))
    i += 1

  df = pd.DataFrame(rows, columns=['dest', 'source', 'num'])
  df['max'] = df['source'] + df['num'] - 1
  df = df.sort_values('source').reset_index(drop=True)
  maps[m[0]][m[1]] = df

  i += 1


def seed_locations(ranges):
  t = 'seed'

  while t != 'location':
    m = maps[t]
    k = list(m.keys())
    assert len(k) == 1
    t = k[0]
    df = m[t]

    next_ranges = []

    for start, end in ranges:
      rows = df[
          ((df['source'] <= start) & (df['max'] >= (start))) |
          ((df['source'] <= end) & (df['max'] >= (end)))
      ].index
      if len(rows):
        rows = df.iloc[rows.min():rows.max()+1]

        if start < rows['source'].min():
          next_ranges.append((start, rows['source'].min() - 1))

        if end > rows['max'].max():
          next_ranges.append((rows['max'].max() + 1, end))

        for i, row in rows.iterrows():
          s = max(row.source, start)
          e = min(row['max'], end)

          next_ranges.append((
            row.dest + s - row.source,
            row.dest + e - row.source
          ))
      else:
        next_ranges.append((start, end))

    ranges = next_ranges

  return ranges


# Part 1
# Part 1 is as special case of part 2 where the length of each range is 1
ranges = [(s, s) for s in seeds]
ranges = seed_locations(ranges)
print("Part 1:", min([r[0] for r in ranges]))

# Part 2
ranges = [(start, start + num - 1) for start, num in (zip(seeds[::2], seeds[1::2]))]
ranges = seed_locations(ranges)
print("Part 2:", min([r[0] for r in ranges]))