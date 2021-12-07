import numpy as np

with open('../input.txt') as f:
    a = np.array([int(x) for x in f.read().strip().split(',')])

# Part 1
print("Part 1:", np.min([np.abs(a - i).sum() for i in range(999)]))

# Part 2
def f(i):
    return i*(i + 1)//2

print("Part 2:", np.min([f(np.abs(a - i)).sum() for i in range(999)]))