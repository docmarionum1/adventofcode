from aoc.common import *

registers, program = read_input(
  delim="\n\n",
)

a, b, c = read_input(
  text=registers,
  mapper=lambda r: int(re.search(r'(\d+)', r).groups()[0])
)

A = 4
B = 5
C = 6
PC = 8

reg = {
    A: a,
    B: b,
    C: c,
    PC: 0,
}

program = tuple(map(int, program[9:].split(",")))

def combo(o):
  return reg.get(o, o)

def dv(o):
  return reg[A] // 2**combo(o)

def adv(o):
  reg[A] = dv(o)

def bxl(o):
  reg[B] = reg[B] ^ o

def bst(o):
  reg[B] = combo(o) % 8

def jnz(o):
  if reg[A] != 0:
    reg[PC] = o
    return True

def bxc(o):
  reg[B] = reg[B] ^ reg[C]

output_buffer = []
def out(o):
  output_buffer.append(combo(o) % 8)

def bdv(o):
  reg[B] = dv(o)

def bdv(o):
  reg[C] = dv(o)

ops = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: bdv,
}

def run(a, b, c):
  output_buffer.clear()
  reg[A] = a
  reg[B] = b
  reg[C] = c
  reg[PC] = 0

  while reg[PC] < len(program):
    if not ops[program[reg[PC]]](program[reg[PC] + 1]):
      reg[PC] += 2

  return tuple(output_buffer)

print("Part 1:", ",".join(map(str, run(a, b, c))))

a = 0
i = 1
while i <= len(program):
  while run(a,b,c)[-i:] != program[-i:]:
    a += 1

  a = a << 3
  i += 1

print("Part 2:", a >> 3)