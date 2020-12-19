import os

from py65asm.assembler import Assembler
from py65emu.cpu import CPU
from py65emu.mmu import MMU

a = Assembler()

f = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "main.asm"
)

out = a.assemble(open(f))
print(out)
for i, ins in enumerate(out):
    print(i, ":", hex(ins))



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

print(len(input_bytes))

#exit()

m = MMU([
        (0x00, 0x200), # Create RAM with 512 bytes
        (0x1000, 0x1000 + len(input_bytes), True, input_bytes), # Input bytes
        (0xC000, 0xFFFF, True, out) # Create ROM starting at 0xC000 with your program.
])

c = CPU(m, 0xC000)

#while not c.r.getFlag('B'): # Run until we break
while m.read(c.r.pc) != 0x1a:
    #print(hex(c.r.pc), hex(m.read(c.r.pc)))    # Program Counter
    #print(hex(c.r.y))
    #print(c.r.a)
    #print(m.read(0), m.read(1))
    try:
        #print(hex(c.r.pc), hex(m.read(c.r.pc)), hex(c.r.s), hex(c.r.y))    # Program Counter
        #print(m.blocks[0])
        c.step()
        #print(hex(c.r.s), hex(m.read(c.stack_page*0x100 + c.r.s)))
    except:
        print("AAA")
        #print(hex(c.r.pc))    # Program Counter
        break

print("\n\n")
print('PC', c.r.pc)
print('A', c.r.a)
print('X', c.r.x)
print('Y', c.r.y)
print(c.r.s)
#print(m.read(0xff), m.read(254), m.read(253), m.read(252), m.read(251), m.read(250))
print(m.blocks[0])
#print(m.read(240), m.read(239), m.read(238))
#print(m.read(3), m.read(2))
#print(hex(m.read(3)), hex(m.read(2)))
# Check the value that's left in the readNumber working memory

print("input_pointer", m.readWord(0))
print("j", m.readWord(8))

print(m.readWord(6))
print(m.readWord(10))
print(m.readWord(0x0c))

print(m.read(0x10) + (m.read(0x11) << 8) + (m.read(0x12) << 16))
