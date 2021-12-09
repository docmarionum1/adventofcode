import numpy as np
from scipy.ndimage.interpolation import shift

with open('../input.txt') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]
a = np.array([[int(i) for i in l] for l in lines])

# Part 1

def is_minima(i, j):
    n = a[i,j]

    if i > 0 and a[i-1,j] <= n:
        return False
    if j > 0 and a[i,j-1] <= n:
        return False
    if i < (len(a) - 1) and a[i+1,j] <= n:
        return False
    if j < (len(a) - 1) and a[i,j+1] <= n:
        return False

    return True

risk_level = 0

for i in range(len(a)):
    for j in range(len(a)):
        if is_minima(i, j):
            #print(j, a[0,j])
            risk_level += 1 + a[i,j]

print(risk_level)

# Part 1 v2

minima = a[(
    (a < shift(a, (0, 1), cval=10)) & 
    (a < shift(a, (1, 0), cval=10)) &
    (a < shift(a, (0, -1), cval=10)) & 
    (a < shift(a, (-1, 0), cval=10))
)]

print(minima.sum() + len(minima))

# Part 2

b = a.copy()
sizes = []

def size_of_region(i, j):
    if b[i, j] in [-1, 9]:
        return 0

    s = 1
    b[i,j] = -1

    if i > 0:
        s += size_of_region(i-1, j)
    if j > 0:
        s += size_of_region(i, j-1)
    if i < (len(a) - 1):
        s += size_of_region(i+1, j)
    if j < (len(a) - 1):
        s += size_of_region(i, j+1)

    return s


for i in range(len(a)):
    for j in range(len(a)):
        s = size_of_region(i,j)
        if s:
            sizes.append(s)

print(np.prod(sorted(sizes)[-3:]))