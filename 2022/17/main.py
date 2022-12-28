import re
import numpy as np

jets = open("input.txt").read().strip()
rocks = [
  [[1, 1, 1, 1]],
  [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
  ],
  [
    [0, 0, 1],
    [0, 0, 1],
    [1, 1, 1],
  ],
  [
    [1],
    [1],
    [1],
    [1],
  ],
  [
    [1, 1],
    [1, 1]
  ],
]

class Simulation:
  def __init__(self):
    self.jet_index = 0
    self.rock_index = 0
    self.room = np.pad(np.zeros((4, 7)), [(0, 1), (1, 1)], constant_values=1)
    self.prev_height = 0
    self.height_sequence = ""

  def pad_rock(self, x, y):
    return np.pad(self.rock, [
      (y, self.room.shape[0] - self.rock.shape[0] - y), 
      (x, self.room.shape[1] - x - self.rock.shape[1])
    ])

  def collision(self, x, y):
    return np.max(self.room + self.pad_rock(x, y)) > 1

  def max_height(self):
    return np.argwhere(self.room[:,1:-1])[:,0].min()

  def rock_height(self):
    return self.room.shape[0] - self.max_height() - 1

  def pad_room(self, h):
    y = 3 + h - self.max_height()
    if y <= 0:
      return self.room
    return np.vstack([
      np.tile(np.pad(np.zeros(7), 1, constant_values=1), (y, 1)),
      self.room
    ])

  def drop_rocks(self, n):
    for i in range(n):
      new_height = self.room.shape[0] - self.max_height() - 1
      self.height_sequence += str(new_height - self.prev_height)
      self.prev_height = new_height
      self.rock = np.array(rocks[self.rock_index])
      self.room = self.pad_room(self.rock.shape[0])
      y = self.max_height() - self.rock.shape[0] - 3
      x = 3
      at_rest = False
      while not at_rest:
        jet = jets[self.jet_index]
        self.jet_index = (self.jet_index + 1) % len(jets)
        if jet == "<" and not self.collision(x - 1, y):
          x -= 1
        if jet == ">" and not self.collision(x + 1, y):
          x += 1
        if self.collision(x, y + 1):
          self.room = self.room + self.pad_rock(x, y)
          self.rock_index = (self.rock_index + 1) % len(rocks)
          break
        else:
          y += 1

    return self

sim = Simulation()
print("Part 1:", sim.drop_rocks(2022).rock_height())

def detect_pattern(height_sequence):
  i = int(len(height_sequence)/2)
  j = i + 1

  while True:
    preamble, pattern, remainder = re.match(f'^(\d*?)({height_sequence[i:j]})+(\d*)?$', height_sequence).groups()
    if len(remainder) < len(pattern):
      break
    j += 1

  return preamble, pattern

def get_height_at(n):
  # Drop some more rocks to an arbitrary height that's "probably" long enough to
  # find our pattern
  height_sequence = sim.drop_rocks(5000-2022).height_sequence
  preamble, pattern = detect_pattern(height_sequence)
  pattern = list(map(int, pattern))
  preamble = list(map(int, preamble))

  n_reps = (n - len(preamble)) // len(pattern)
  remainder = n - (len(preamble) + n_reps * len(pattern))

  return sum(preamble) + n_reps * sum(pattern) + sum(pattern[:remainder+1])

print("Part 2:", get_height_at(1000000000000))