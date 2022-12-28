from ortools.sat.python import cp_model

blueprints = open('input19.txt').read().splitlines()

def lp(costs, n, *args):
  costs = costs.T
  inventories = [np.array([0, 0, 0, 0])]
  robots = [np.array([1, 0, 0, 0])]
  model = cp_model.CpModel()

  for t in range(n):
    inventory = inventories[-1]
    robot = robots[-1]

    build_robot = np.array([
        model.NewIntVar(0, 1, r) for r in order
    ])

    model.Add(sum(build_robot) <= 1)
    cost = (build_robot*costs).sum(axis=1)
    inventory = inventory - cost
    for r in inventory:
      model.Add(r >= 0)
    inventory = inventory + robot
    robot = robot + build_robot
    robots.append(robot)
    
    inventories.append(inventory)

  model.Maximize(inventories[-1][-1])
  solver = cp_model.CpSolver()
  res = solver.Solve(model)
  return solver.ObjectiveValue()

print("Part 1:", int(sum([i*g for i,g in solve(blueprints, 24, lp)])))
print("Part 2:", int(np.product([g for i,g in solve(blueprints[:3], 32, lp)])))