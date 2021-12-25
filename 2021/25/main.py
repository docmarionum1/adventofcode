with open('input.txt') as f:
    lines = [[c for c in line.strip()] for line in f.readlines()]

h, w = len(lines), len(lines[0])

def move(c):
    ni = lambda i: (i + 1) % w if c == ">" else i
    nj = lambda j: (j + 1) % h if c == "v" else j

    to_move = []
    for j in range(h):
        for i in range(w):
            if lines[j][i] == c and lines[nj(j)][ni(i)] == ".":
                to_move.append((i, j))

    for i, j in to_move:
        lines[j][i] = "."
        lines[nj(j)][ni(i)] = c

    return len(to_move)

num_moves = 1
while (move(">") + move("v")) > 0:
    num_moves += 1

print(num_moves)