points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

opening = "([{<"
closing = ")]}>"

def parse_line(line):
    stack = []

    for c in line:
        if c in opening:
            stack.append(c)
        else:
            if c != closing[opening.index(stack.pop())]:
                return (points[c], 0)
                
    score = 0
    while stack:
        score = score * 5 + opening.index(stack.pop()) + 1 

    return (0, score)

corrupt_score = 0
incomplete_scores = []
with open('../input.txt') as f:
    for line in f.readlines():
        c, i = parse_line(line.strip())
        corrupt_score += c
        if i:
            incomplete_scores.append(i)


print("Part 1:", corrupt_score)
print("Part 2:", sorted(incomplete_scores)[len(incomplete_scores)//2])