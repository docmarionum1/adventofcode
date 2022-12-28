import numpy as np
from scipy.ndimage import generic_filter
from scipy.ndimage.measurements import label

coords = open('input.txt').read().splitlines()
coords = [tuple(map(int, c.split(","))) for c in coords]

# Create the grid
coords = np.array(coords)
grid = np.zeros(coords.max(axis=0)+2) # +2 to give buffer around the edges
for x,y,z in coords:
  grid[x,y,z] = 1

def count_open_faces(window):
  window = window.reshape((3,3,3))
  return window[1,1,1]* (6 - (
    window[0, 1, 1] + window[2, 1, 1] + window[1, 0, 1] + window[1, 2, 1] + window[1, 1, 0] + window[1, 1, 2]
  ))

# Perform a 3D convolution to count the empty faces at each coordinate
print("Part 1:", generic_filter(grid, count_open_faces, size=3, mode="constant", cval=0).sum().astype(int))

# Use the label function to find the continuous same-value areas
# Anything on the outside of the blob will be in the same blob
# Replace the values that aren't in that blob and then count the same as above
filled_grid = (label(grid == 0)[0] != 1).astype(int)
print("Part 2:", generic_filter(filled_grid, count_open_faces, size=3, mode="constant", cval=0).sum())