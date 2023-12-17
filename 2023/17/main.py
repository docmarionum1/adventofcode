from aoc.common import *

grid = read_grid().astype(int)

h, w = grid.shape
max_i = h - 1
max_j = w - 1
dest = (h-1, w-1)


def shortest_path(maxt, mint):
  heap = [
    (grid[0,1], (0, 1, 'r', 1)),
    (grid[1,0], (1, 0, 'd', 1)),
  ]
  visited = {}
  dest_dist = np.inf

  while heap:
    dist, (i, j, direction, steps) = heapq.heappop(heap)
    node = (i, j, direction, steps)

    if dest_dist < dist:
      break

    if (i,j) == dest and steps >= mint and steps <= maxt and dist < dest_dist:
      dest_dist = dist

    if node not in visited:
      visited[node] = dist
    else:
      if (visited[node] > dist):
        visited[node] = dist
      
      continue

    # Right
    if j < max_j and (direction != 'l') and ((direction == 'r' and steps < maxt) or (direction != 'r' and steps >= mint)):
      heapq.heappush(heap, (dist + grid[i,j+1], (i, j+1, 'r', 1 if direction != 'r' else steps + 1)))

    # Left
    if j > 0 and (direction != 'r') and ((direction == 'l' and steps < maxt) or (direction != 'l' and steps >= mint)):
      heapq.heappush(heap, (dist + grid[i,j-1], (i, j-1, 'l', 1 if direction != 'l' else steps + 1)))

    # Down
    if i < max_i and (direction != 'u') and ((direction == 'd' and steps < maxt) or (direction != 'd' and steps >= mint)):
      heapq.heappush(heap, (dist + grid[i+1,j], (i+1, j, 'd', 1 if direction != 'd' else steps + 1)))

    # Up
    if i > 0 and (direction != 'd') and ((direction == 'u' and steps < maxt) or (direction != 'u' and steps >= mint)):
      heapq.heappush(heap, (dist + grid[i-1,j], (i-1, j, 'u', 1 if direction != 'u' else steps + 1)))

  return dest_dist 

print("Part 1:", shortest_path(3, 0))
print("Part 2:", shortest_path(10, 4))