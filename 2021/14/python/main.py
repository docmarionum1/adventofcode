# Day 14

with open('../input.txt') as f:
    template = f.readline().strip()
    f.readline()

    rules = dict([l.strip().split(" -> ") for l in f.readlines()])

memo = {}

def expand(pair, steps):
    if (pair, steps) in memo:
        return memo[(pair, steps)].copy()

    if steps == 0:
        return {}

    middle = rules[pair]

    result = expand(pair[0] + middle, steps-1)
    result_right = expand(middle + pair[1], steps-1)

    for k,v in result_right.items():
        result[k] = result.get(k, 0) + v

    result[middle] = result.get(middle, 0) + 1

    memo[(pair, steps)] = result.copy()

    return result

def get_counts(steps):
    counts = {}
    for c in template:
        counts[c] = counts.get(c, 0) + 1

    for i in range(len(template)-1):
        pair = template[i:i+2]
        result = expand(pair, steps)

        for k,v in result.items():
            counts[k] = counts.get(k, 0) + v

    counts_list = sorted(counts.items(), key=lambda p: p[1])
    return counts_list[-1][1] - counts_list[0][1]

print("Part 1:", get_counts(10))
print("Part 2:", get_counts(40))