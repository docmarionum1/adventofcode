from aoc.common import *

# !pip install ortools
from ortools.sat.python import cp_model

def parse_machine(machine):
  a, b, prize = map(
      lambda s: tuple(map(int, re.match(r'.*: X[+=](\d+), Y[+=](\d+)', s).groups())),
      machine.split("\n")
  )

  return a, b, prize

machines = read_input(
    delim="\n\n", mapper=parse_machine
)

def solve(offset):
  cost = 0
  for (ax, ay), (bx, by), (px, py) in machines:
    model = cp_model.CpModel()
    a = model.new_int_var(0, 100+offset, "a")
    b = model.new_int_var(0, 100+offset, "b")

    model.add(ax*a + bx*b == px + offset)
    model.add(ay*a + by*b == py + offset)

    model.minimize(3*a + b)

    try:
      solver = cp_model.CpSolver()
      solver.solve(model)
      cost += solver.objective_value
    except:
      pass

  return int(cost)

print("Part 1:", solve(0))
print("Part 2:", solve(10000000000000))