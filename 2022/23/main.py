import numpy as np

grid = open('input.txt').read().splitlines()
grid = np.array(list(map(lambda row: [0 if v == '.' else 1 for v in row], grid)))
grid = np.pad(grid, grid.shape)

order = ['N', 'S', 'W', 'E']
order_index = 0

round = 1
while True:
  proposed_moves_dict = {}

  for coords in np.argwhere(grid):
    i, j = coords
    window = grid[i-1:i+2,j-1:j+2]

    if window.sum() == 1:
      continue

    new_coords = None
    for oi in range(4):
      direction = order[(order_index+oi)%4]
      if direction == "N" and window[0,:].sum() == 0:
          new_coords = [coords[0]-1, coords[1]]
      if direction == "S" and window[2,:].sum() == 0:
          new_coords = [coords[0]+1, coords[1]]
      if direction == "W" and window[:,0].sum() == 0:
          new_coords = [coords[0], coords[1]-1]
      if direction == "E" and window[:,2].sum() == 0:
          new_coords = [coords[0], coords[1]+1]
      if new_coords:
        break

    if new_coords:
      proposed_moves_dict.setdefault(tuple(new_coords), []).append(tuple(coords))

  if len(proposed_moves_dict) == 0:
    print("Part 2:", round)
    break

  for new_coords, coords_list in proposed_moves_dict.items():
    if len(coords_list) > 1:
      continue
    coords = coords_list[0]
    grid[coords[0],coords[1]] = 0
    grid[new_coords[0],new_coords[1]] = 1

  if round == 10:
    nz = np.nonzero(grid)
    trimmed = grid[nz[0].min():nz[0].max()+1,nz[1].min():nz[1].max()+1]
    print("Part 1:", (trimmed == 0).sum())

  round += 1
  order_index = (order_index + 1) % 4