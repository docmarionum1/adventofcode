import numpy as np
import re

pattern = r'([onf]+) x=(-*\d+)..(-*\d+),y=(-*\d+)..(-*\d+),z=(-*\d+)..(-*\d+)'

lines = list(map(lambda l: re.match(pattern, l).groups(), open('input.txt').readlines()))

def parse_line(line):
    i, *nums = line
    i = i == 'on'
    x0, x1, y0, y1, z0, z1 = map(lambda n: int(n), nums)
    x0, x1 = sorted([x0, x1])
    y0, y1 = sorted([y0, y1])
    z0, z1 = sorted([z0, z1])

    return i, (x0, x1, y0, y1, z0, z1)

def intersects(a, b):
    return (
        (a[1] >= b[0]) and 
        (a[0] <= b[1]) and 
        (a[3] >= b[2]) and
        (a[2] <= b[3]) and
        (a[5] >= b[4]) and
        (a[4] <= b[5])
    )

def get_overlap(a, b):
    if intersects(a, b):
        return (
            max(a[0], b[0]), min(a[1], b[1]),
            max(a[2], b[2]), min(a[3], b[3]),
            max(a[4], b[4]), min(a[5], b[5])
        )

def volume(a):
    return (a[1] + 1 - a[0]) * (a[3] + 1 - a[2]) * (a[5] + 1 - a[4])

regions = []

count = 0
for line_num, line in enumerate(lines):
    i, cube = parse_line(line)

    new_regions = []
    if i:
        new_regions.append((i, cube))
        count += volume(cube)

    for j, cube2 in regions:
        o = get_overlap(cube, cube2)
        if o is not None:
            if i and j:
                new_regions.append((False, o))
                count -= volume(o)
            elif (not i) and (not j):
                new_regions.append((True, o))
                count += volume(o)
            elif (not i) and j:
                new_regions.append((False, o))
                count -= volume(o)
            elif i and (not j):
                new_regions.append((True, o))
                count += volume(o)

    regions += new_regions

    if line_num == 19: # Works for me
        print("Part 1:", count)
        
print("Part 2:", count)