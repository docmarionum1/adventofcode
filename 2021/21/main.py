import numpy as np
from functools import lru_cache
from itertools import product

class DeterministicDie:
    def __init__( self ):
        self.num_rolls = 0
        self.i = 0
    def __next__( self):
        self.num_rolls += 1
        r = self.i + 1
        self.i = (self.i + 1) % 100
        return r

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.score = 0

die = DeterministicDie()

def roll3():
    return next(die) + next(die) + next(die)

players = [Player(4), Player(6)]

def round():
    for player in players:
        player.pos = (player.pos - 1 + roll3()) % 10 + 1
        player.score += player.pos

        if player.score >= 1000:
            return False

    return True

while round():
    pass

print("Part 1", min([p.score for p in players]) * die.num_rolls)

def roll3():
    die = [1, 2, 3]
    return product(die, die, die)

@lru_cache(None)
def num_wins(p1_pos, p1_score, p2_pos, p2_score, turn):
    if p1_score >= 21:
        return np.array([1, 0])
    elif p2_score >= 21:
        return np.array([0, 1])

    res = np.array([0, 0])
    if not turn: # when turn is false, it's p1's turn
        for(i, j, k) in roll3():
            new_pos = (p1_pos + i + j + k - 1) % 10 + 1
            res += num_wins(
                new_pos, p1_score + new_pos,
                p2_pos, p2_score,
                not turn
            )
    else:
        for(i, j, k) in roll3():
            new_pos = (p2_pos + i + j + k - 1) % 10 + 1
            res += num_wins(
                p1_pos, p1_score,
                new_pos, p2_score + new_pos,
                not turn
            )

    return res

print("Part 2:", num_wins(4, 0, 6, 0, False).max())