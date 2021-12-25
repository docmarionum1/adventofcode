import numpy as np
from scipy import signal

def binify(line):
    return [1 if c == "#" else 0 for c in line.strip()]

grid = []
with open('input.txt') as f:
    enhance = binify(f.readline())
    f.readline()
    for line in f.readlines():
        grid.append(binify(line))

grid = np.array(grid)

def enhance_algo(n):
    return enhance[int(str(n), 2)]

enhance_algo = np.vectorize(enhance_algo)

kernel = np.array([
    [10**0, 10**1, 10**2],
    [10**3, 10**4, 10**5],
    [10**6, 10**7, 10**8]
])

for i in range(50):
    # I don't know if this works in general, but for my input all 0s make 1s and all 1s make 0s
    # So I can flip back and forth between 0 and 1 as the fillvalue for the rest of space.
    conv = signal.convolve2d(grid, kernel, fillvalue=i%2)
    grid = enhance_algo(conv)

    if i == 1:
        print("Part 1:", grid.sum())

print("Part 2:", grid.sum())