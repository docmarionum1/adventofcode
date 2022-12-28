import re
import numpy as np

blueprints = open('input19.txt').read().splitlines()
order = ["ore", "clay", "obsidian", "geode"]

memo = {}
max_max_geodes = 0
def sim(costs, time_remaining, robots, inventory, last_can_build, last_built):
  global max_max_geodes

  if time_remaining == 0:
    return inventory[-1]

  key = (time_remaining, tuple(robots), tuple(inventory))
  if key in memo:
    return memo[key]

  can_build = (inventory - costs >= 0).all(axis=1)
  max_geodes = sim(costs, time_remaining - 1, robots, inventory + robots, can_build, None)
  for i, cost in enumerate(costs):
    # Check if this branch is definitely non-optimal
    if (inventory[-1] + robots[-1]*time_remaining + time_remaining * (time_remaining - 1) / 2) < max_max_geodes:
      return inventory[-1]

    # Don't build more robots than you could possibly use
    if (i != 3) and ((inventory[i] + robots[i]*time_remaining) / time_remaining) >= costs.max(axis=0)[i]:
      continue

    # Don't build a robot if you could have built it last time but built nothing
    if (last_can_build[i] == True) and (last_built == None):
      continue

    if ((inventory - cost) >= 0).all():
      build = np.zeros(4)
      build[i] = 1
      max_geodes = max(max_geodes, sim(
          costs,
          time_remaining - 1, 
          robots + build,
          inventory - cost + robots,
          can_build,
          i
      ))
    
  memo[key] = max_geodes
  max_max_geodes = max(max_geodes, max_max_geodes)
  return max_geodes

def solve(blueprints, n, solver):
  global memo, max_max_geodes

  results = []
  for i, blueprint in enumerate(blueprints):
    costs = re.findall(r'Each (\w+) robot costs ([a-z0-9 ]+)\.', blueprint)
    costs_list = []
    for rtype, cost in costs:
      if "and" in cost:
        cost = cost.split(" and ")
      else:
        cost = [cost]

      cost = dict(map(lambda c: ( c[1], int(c[0]),), [c.split(' ') for c in cost]))
      cost = np.array([cost.get(rt, 0) for rt in order])
      costs_list.append(cost)
    
    costs_list = np.array(costs_list)

    memo = {}
    max_max_geodes = 0
    geodes = solver(
      costs_list, n, 
      np.array([1, 0, 0, 0]), 
      np.array([0, 0, 0, 0]), 
      np.array([False, False, False, False]), None
    )
    results.append((i+1, geodes))

  return results

print("Part 1:", int(sum([i*g for i,g in solve(blueprints, 24, sim)])))
print("Part 2:", int(np.product([g for i,g in solve(blueprints[:3], 32, sim)])))