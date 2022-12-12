instructions = open("input.txt").read().splitlines()
interesting_cycles = list(range(20, 221, 40))

cycle = 0
x = 1
total_strength = 0
crt = ""

def step():
  global total_strength, crt
  if cycle in interesting_cycles:
    total_strength += x * cycle

  crt_pos = (cycle - 1) % 40
  if (crt_pos >= (x - 1)) and (crt_pos <= (x + 1)):
    crt += "#"
  else:
    crt += "."

for i in instructions:
  cycle += 1
  step()
  if i != "noop":
    v = int(i.split(" ")[1])
    cycle += 1
    step()
    x += v

print("Part 1:", total_strength)
print("Part 2:")
print('\n'.join([crt[i:i+40] for i in range(0, 241, 40)]))