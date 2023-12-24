from aoc.common import *
from sympy import Symbol, solve, symbols

def parse(l):
  p, v = split(l, '@')
  return split(p, ',', int) + split(v, ',', int)

hail = read_input(mapper=parse)

test_area = (200000000000000, 400000000000000)

count = 0
for (a, b) in itertools.combinations(hail, 2):
  pxa, pya, pza, vxa, vya, vza = a
  pxb, pyb, pzb, vxb, vyb, vzb = b

  try:
    x = (pyb - pya + (vya*pxa)/vxa - (vyb*pxb)/vxb) / (vya/vxa - vyb/vxb)
    y = pya + vya * ((x -pxa) / vxa)

    ta = (x - pxa) / vxa
    tb = (x - pxb) / vxb

    # Todo check for the past
    if ta >= 0 and tb >= 0:
      if x >= test_area[0] and x <= test_area[1] and y >= test_area[0] and y <= test_area[1]:
        count += 1
  except ZeroDivisionError:
    pass

print("Part 1:", count)


x, y, z, vx, vy, vz = symbols("x y z vx vy vz")
syms = [x, y, z, vx, vy, vz]
equations = []

# We only need to consider at most 3 of the hailstones to have enough equations
# We start with 6 unknowns, each hailstone adds one more unknown but has 3 equations
# 6 + 3 == 3 * 3
# It works with more, but the more we add the longer it takes
for i, (pxa, pya, pza, vxa, vya, vza) in enumerate(hail[:3]):
  tr = Symbol(f"tr{i}", positive=True)
  syms.append(tr)

  equations = equations + [
      pxa + vxa * tr - x - vx * tr,
      pya + vya * tr - y - vy * tr,
      pza + vza * tr - z - vz * tr,
  ]

d = solve(equations, syms, dict=True)

print("Part 2:", d[0][x] + d[0][y] + d[0][z])