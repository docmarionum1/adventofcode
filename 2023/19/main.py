from aoc.common import *

rules, parts = read_input(delim='\n\n', mapper=lambda b: read_input(text=b))

def parse_part(part):
  return dict((p.split('=')[0], int(p.split('=')[1])) for p in  part[1:-1].split(","))

def parse_rule(rule):
  name, steps = re.match(r'([a-z]+)\{(.*)\}', rule).groups()
  steps = steps.split(',')
  return (name, steps)

parts = list(map(parse_part, parts))
rules = {name: steps for name, steps in map(parse_rule, rules)}

def valid_part(part):
  for r in part.values():
    if len(r) == 0:
      return False

  return True

def apply_rules(rule_name, part, accepted):
  if rule_name == "A":
    accepted.append(part)
    return
  if rule_name == "R":
    return

  steps = rules[rule_name]

  for step in steps:
    if ":" in step:
      v, comp, val, target = re.match(r'([xmas])([<>])(\d+):([a-zA-Z]+)', step).groups()
      val = int(val)

      part2 = {k:np.array(v) for k,v in part.items()}

      if comp == ">":
        part2[v] = part2[v][part2[v] > val]
        if valid_part(part2):
          apply_rules(target, part2, accepted)

        part[v] = part[v][part[v] <= val]

      elif comp == "<":
        part2[v] = part2[v][part2[v] < val]
        if valid_part(part2):
          apply_rules(target, part2, accepted)

        part[v] = part[v][part[v] >= val]

      if not valid_part(part):
        break

    else:
      rule_name = step
      apply_rules(rule_name, part, accepted)

def part1():
  accepted = []
  for part in parts:
    apply_rules("in", {k: np.array([v]) for k,v in part.items()}, accepted)
  print("Part 1:", sum(sum(p.values()) for p in accepted)[0])

def part2():
  accepted = []
  apply_rules("in", {k: np.arange(1, 4001) for k in "xmas"}, accepted)
  print("Part 2:", sum(np.product([len(v) for v in a.values()]) for a in accepted))

part1()
part2()