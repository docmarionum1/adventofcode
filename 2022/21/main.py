from sympy import Symbol, solve

def get_root(variables, part2):
  monkiesq = monkies = open('input.txt').read().splitlines()
  while monkiesq:
    m = monkiesq.pop(0)
    mname, v = m.split(":")
    if mname in variables:
      continue 
    a, *b = v.strip().split(" ")
    if not b:
      variables[mname] = int(a)
    else:
      op, b = b
      if a in variables and b in variables:
        if part2 and mname == "root":
          op = "-"
        if op == "+":
          variables[mname] = variables[a] + variables[b]
        elif op == "-":
          variables[mname] = variables[a] - variables[b]
        elif op == "*":
          variables[mname] = variables[a] * variables[b]
        elif op == "/":
          variables[mname] = variables[a] / variables[b]
      else:
        monkiesq.append(m)
  return variables["root"]

print("Part 1:", int(solve(Symbol("root") - get_root({}, False))[0]))
print("Part 2:", int(solve(get_root({"humn": Symbol("humn")}, True))[0]))