from aoc.common import *

rules, updates = read_input(
    delim="\n\n"
)

rules = read_input(
    text=rules,
    mapper=functools.partial(split_strip, delim="[|]", mapper=int)
)

updates = read_input(
    text=updates,
    mapper=functools.partial(split_strip, delim=",", mapper=int)
)

def apply_rules(update, reorder=False):
  triggered = False
  for rule in rules:
    if rule[0] in update and rule[1] in update:
      if update.index(rule[0]) > update.index(rule[1]):
        triggered = True
        if reorder:
          (
              update[update.index(rule[0])],
              update[update.index(rule[1])]
          ) = rule[1], rule[0]
        else:
          return True

  return triggered

s = 0
invalid = []
for update in updates:
  if not apply_rules(update):
    s += update[len(update)//2]
  else:
    invalid.append(update)

print("Part 1:", s)

s = 0
for update in invalid:
  while apply_rules(update, True):
    pass
  s += update[len(update)//2]

print("Part 2:", s)