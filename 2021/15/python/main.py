import numpy as np
import networkx as nx

with open('../input.txt') as f:
    lines = f.readlines()

m = np.array([list(l.strip()) for l in lines]).astype(int)

def get_shortest_path(map):
    def get_neighbors(i, j):
        neighbors = []
        for (x, y) in [
                    (i - 1, j),
                    (i + 1, j),
                    (i, j - 1),
                    (i, j + 1)
        ]:
            if (
                (x >= 0) and
                (x < map.shape[1]) and
                (y >= 0) and
                (y < map.shape[1])
            ):
                neighbors.append(((i, j), (x, y), map[y][x]))

        return neighbors

    G = nx.DiGraph()
    for i in range(map.shape[1]):
        for j in range(map.shape[0]):
            for a, b, weight in get_neighbors(i, j):
                G.add_edge(a, b, weight=weight)

    return nx.shortest_path_length(G, (0, 0), (map.shape[0]-1, map.shape[1]-1), weight='weight')

print("Part 1:", get_shortest_path(m))

def inc(map, i):
    new_map = (map.copy() + i) % 10
    return np.where(new_map < map, new_map + 1, new_map)

full_map = np.hstack([inc(m, i) for i in range(5)])
full_map = np.vstack([inc(full_map, i) for i in range(5)])

print(full_map[-1])

print("Part 2:", get_shortest_path(full_map))