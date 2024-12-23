# Common imports
import cmath
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import functools
import math
import os
import re
import string
import itertools
import networkx as nx
import heapq
from typing import Literal

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from tqdm.contrib.concurrent import process_map


# Helper functions
def process_input(inp, mapper=None, delim='\n', strip=True, **kwargs):
  if strip:
    inp = inp.strip()

  if delim:
    lines = inp.split(delim)
  else:
    return inp

  if mapper:
    lines = list(map(mapper, lines))

  return lines


def read_input(filename='input.txt', text=None, **kwargs):
  if not text:
    text = open(filename).read()

  return process_input(text, **kwargs)

def split_strip(string, delim=" ", mapper=lambda x: x):
  return [mapper(s.strip()) for s in re.split(delim, string.strip())]

split = split_strip

def map2(t, f1=lambda x: x, f2=lambda x: x):
  """Given an iterable of length 2, map f1 to t[0] and f2 to t[1]."""
  t = list(t)
  assert len(t) == 2

  return f1(t[0]), f2(t[1])

def grid_to_nx(grid, invalid_char="#", neighbor_data=None, **kwargs):
  G = nx.DiGraph()
  for cell, value in grid.items():
    for n in neighbors(cell, data=neighbor_data):
      if isinstance(n, tuple):
        n, data = n
        attr = {neighbor_data: data}
      else:
        attr = {}

      if grid.get(n, invalid_char) != invalid_char:
        G.add_edge(cell, n, **attr)
  return G

def read_grid(return_type: Literal["np", "dict", "nx"] = "np", **kwargs):
  grid = np.array(read_input(**kwargs, mapper=list))

  if return_type == "dict":
    return np_grid_to_dict(grid)
  elif return_type == "nx":
    return grid_to_nx(np_grid_to_dict(grid), **kwargs)
  elif return_type == "np":
    return grid

def print_dict_grid(grid):
  np_grid = np.zeros((
      int(max([i.real for i in grid.keys()])) + 1,
      int(max([i.imag for i in grid.keys()])) + 1
  )).astype(str)
  for (j,i), value in np.ndenumerate(np_grid):
    np_grid[(j,i)] = grid.get(complex(j,i), ".")

  print_grid(np_grid)

def print_grid(grid):
  if isinstance(grid, dict):
    print_dict_grid(grid)
  else:
    print("\n".join(["".join(map(str, g)) for g in grid]))

def np_grid_to_dict(grid):
  return {complex(j,i): grid[j,i] for j, i in np.ndindex(grid.shape)}

def neighbors(a, include_diagonals=False, data=None):
  n = [a + 1j, a + 1, a - 1j, a - 1]

  if data == "compass":
    return list(zip(n, ["E", "S", "W", "N"]))
  elif data == "arrow":
    return list(zip(n, [">", "v", "<", "^"]))
  else:
    return n

def make_grid(h, w):
  return {complex(j,i): "." for j in range(h) for i in range(w)}

def make_nx_grid(h, w):
  G = nx.DiGraph()
  for j in range(h):
    for i in range(w):
      node = complex(j, i)
      for n in neighbors(node):
        if n.real >= 0 and n.real < h and n.imag >= 0 and n.imag < w:
          G.add_edge(node, n)
  return G