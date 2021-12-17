# Day 17
# target area: x=244..303, y=-91..-54

target_x = [244, 303]
target_y = [-91, -54]

def f(x, y, t):
    if t == 0:
        return [0, 0]

    prev = f(x, y, t - 1)

    prev[0] += max(0, x - t + 1)
    prev[1] += (y - t + 1)

    return prev

# Part 1: You always pass through y = 0 on the way down
# So to get max height, initial y = lowest y of target area - 1
ys = []
i = 0
while True:
    y = f(0, abs(target_y[0]) - 1, i)[1]
    ys.append(y)

    if y < target_y[0]:
        break

    i += 1

print("Part 1:", max(ys))

# Part 2

def is_valid(x, y):
    i = 0
    while True:
        p = f(x, y, i)

        if (p[0] > target_x[1]) or (p[1] < target_y[0]):
            return False

        if (p[0] >= target_x[0]) and (p[1] >= target_y[0]) and (p[0] <= target_x[1]) and (p[1] <= target_y[1]):
            return True

        i += 1

options = []
x = 0
for x in range(0, target_x[1]+1):
    for y in range(target_y[0], abs(target_y[0])):
        if is_valid(x, y):
            options.append((x, y))

print("Part 2", len(options))