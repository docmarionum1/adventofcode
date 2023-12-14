# Common imports
import cmath
from collections import defaultdict
import functools
import math
import re
import string
import itertools

import numpy as np
import pandas as pd


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


# Graveyard; weren't necessary but maybe useful later

def consumes_all(numbers, pattern):
  i = 0
  j = 0
  while j < len(numbers):
    if pattern[i % len(pattern)] != numbers[j]:
      return False

    i += 1
    j += 1

  return True

def find_pattern(df):
  numbers = df[1].values
  string = ','.join(df[1].astype(str))

  for i in range(len(numbers)):
    for j in range(i+1, len(numbers)):
      substring = ','.join(numbers[i:j].astype(str))
      if string.count(substring) == 1:
        break

      if (
        string.count(substring) > 1 and
        string.count(substring+","+substring) > 0 and
        consumes_all(numbers[i:], numbers[i:j])
      ):
        return numbers[i:j]