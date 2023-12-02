# Common imports
import re

import numpy as np

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
  

def read_input(filename='input.txt', **kwargs):
  inp = open(filename).read()

  return process_input(inp, **kwargs)

def split_strip(string, delim=" "):
  return [s.strip() for s in string.strip().split(delim)]

def map2(t, f1=lambda x: x, f2=lambda x: x):
  """Given an iterable of length 2, map f1 to t[0] and f2 to t[1]."""
  t = list(t)
  assert len(t) == 2

  return f1(t[0]), f2(t[1])