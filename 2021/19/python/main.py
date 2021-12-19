import itertools
import math

import numpy as np
from numpy import cross, eye, dot
from scipy.linalg import expm, norm

# Get the transformation matrix for rotating a point around axis by theta
def M(axis, theta):
    return expm(cross(eye(3), axis/norm(axis)*theta))

# Return points rotated by xrot, yrot and zrot radians
def rot3(points, xrot, yrot, zrot):
  if xrot:
    M0 = M([1, 0, 0], xrot)
    points = np.array(list(map(lambda p: dot(M0, p), points)))

  if yrot:
    M0 = M([0, 1, 0], yrot)
    points = np.array(list(map(lambda p: dot(M0, p), points)))

  if zrot:
    M0 = M([0, 0, 1], zrot)
    points = np.array(list(map(lambda p: dot(M0, p), points)))

  return points

# Euclidean distance
def dist(a, b):
  return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

# Get all of the distances between each pair of points within a scanner
def get_dists(scanner):
  dists = []
  for i in range(len(scanner)):
    dists.append([dist(scanner[i], scanner[j]) for j in range(len(scanner))])
  return dists

# Find a transformation from pointcloud a to b if one exists
def get_transformation(a, b):
  dists_0 = get_dists(a)
  dists_1 = get_dists(b)

  common_points = []

  for (i, j) in itertools.product(range(len(dists_0)), range(len(dists_1))):
    same = 0
    for (k, l) in itertools.product(dists_0[i], dists_1[j]):
      if k == l:
        same += 1

        if same == 12:
          common_points.append((a[i], b[j]))
          break

  if common_points:
    common_points = np.array(common_points)

    for xrot in [0, np.pi/2, np.pi, np.pi*1.5]:
      for yrot in [0, np.pi/2, np.pi, np.pi*1.5]:
        for zrot in [0, np.pi/2, np.pi, np.pi*1.5]:
          points = rot3(common_points[:,1], xrot, yrot, zrot)

          d = (common_points[:,0] - points).round().astype(int)

          if len(np.unique(d, axis=0)) == 1:
            return xrot, yrot, zrot, d[0]

scanners = []
scanner = []

# Read input
with open('../input.txt') as f:
  for line in f.readlines():
    line = line.strip()
    if line == "":
      scanners.append(scanner)
    elif line[0:2] == "--":
      scanner = []
    else:
      scanner.append(tuple([int(d) for d in line.split(",")]))

scanners.append(scanner)

# Track the full set of beacons
beacons = list(set(scanners.pop(0)))

# Track the locations of each scanner for part 2
scanner_locations = [np.array([0, 0, 0])]

while scanners:
  scanner = scanners.pop(0)
  result = get_transformation(beacons, scanner)
  if result is not None:
    xrot, yrot, zrot, d = result
    points = rot3(scanner, xrot, yrot, zrot)
    v = list(map(lambda p: tuple((p + d).round().astype(int)), points))

    beacons = list(set(beacons + v))

    scanner_locations.append(d)
  else:
    scanners.append(scanner)

print("Part 1:", len(beacons))

max_distance = 0
for (a, b) in itertools.combinations(scanner_locations, 2):
  d = np.abs(a - b).sum()
  max_distance = max(max_distance, d)

print("Part 2:", max_distance)