import os

from py65asm.assembler import Assembler
from py65emu.cpu import CPU
from py65emu.mmu import MMU


# Assemble the program
a = Assembler()

f = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "main.asm"
)

out = a.assemble(open(f))

# Put the input into an array
input_path = '../input.txt'
with open(input_path, 'rb') as f:
    input_bytes = []
    b = f.read(1)
    while b:
        input_bytes.append(ord(b))
        b = f.read(1)

# Add another new line to terminate
input_bytes += [10]

# Initialize memory and the CPU
m = MMU([
        (0x00, 0x200), # Create RAM with 512 bytes
        (0x1000, 0x1000 + len(input_bytes), True, input_bytes), # Input bytes
        (0xC000, 0xFFFF, True, out) # Create ROM starting at 0xC000 with your program.
])

c = CPU(m, 0xC000)

while not c.r.getFlag('B'): # Run until we break
    c.step()

# Print out the 3-byte answer as decimal
print(m.read(0x10) + (m.read(0x11) << 8) + (m.read(0x12) << 16))
