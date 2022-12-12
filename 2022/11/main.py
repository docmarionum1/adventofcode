import math
import re

rules = open("input.txt").read()

class Monkey:
  def __init__(self, id, items, operator, test, t, f, manage_worry):
    self.id = id
    self.items = items
    self.operator = operator
    self.test = test
    self.true = t
    self.false = f
    self.num_inspected = 0
    self.manage_worry = manage_worry

  def turn(self):
    while self.items:
      self.num_inspected += 1
      item = self.items.pop(0)
      item = self.operator(item)
      item = self.manage_worry(item)
      if item % self.test == 0:
        monkies[self.true].items.append(item)
      else:
        monkies[self.false].items.append(item)

pattern = r'''Monkey (\d+):
  Starting items: ([0-9 ,]+)
  Operation: new = (old|\d+) (\+|\*) (old|\d+)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)'''

def make_monkies(manage_worry):
  monkies = {}

  for monkey_rules in re.findall(pattern, rules):
    def get_operator(A, operation, B):
      def f(old):
        a = old if A == "old" else int(A)
        b = old if B == "old" else int(B)
        if operation == "+":
          return a + b
        return a * b
      return f

    monkey = Monkey(
        int(monkey_rules[0]), #id
        list(map(int, monkey_rules[1].split(", "))), # Starting items
        get_operator(*monkey_rules[2:5]), #operator
        int(monkey_rules[5]), #test
        int(monkey_rules[6]), #true throw
        int(monkey_rules[7]), # False throw
        manage_worry, # Manage worry function
    )

    monkies[monkey.id] = monkey

  return monkies

def sim(n):
  global monkies

  if n == 20:
    manage_worry = lambda v: v // 3
  else:
    MOD = math.prod([m.test for m in monkies.values()])
    manage_worry = lambda v: v % MOD

  monkies = make_monkies(manage_worry)

  for round in range(n):
    for i in range(len(monkies)):
      monkies[i].turn()

  return math.prod(sorted([m.num_inspected for m in monkies.values()])[-2:])

print("Part 1:", sim(20))
print("Part 2:", sim(10000))