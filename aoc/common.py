# Common imports
import cmath
from collections import defaultdict
import functools
import math
import re
import string
import itertools
import networkx as nx
import heapq

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from tqdm.contrib.concurrent import process_map


# Helper functions
def process_input(inp, mapper=None, delim='\n', strip=True):
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

def read_grid(**kwargs):
  return np.array(read_input(**kwargs, mapper=list))

def print_grid(grid):
  print("\n".join(["".join(g) for g in grid]))

def np_grid_to_dict(grid):
  return {(j,i): grid[j,i] for j, i in np.ndindex(grid.shape)}

def neighbors(j, i, include_diagonals=False):
  n = [(j+1, i), (j-1, i), (j, i+1), (j, i-1)]
  if include_diagonals:
    n += [(j+1, i+1), (j+1, i-1), (j-1, i+1), (j-1, i-1)]
  return n