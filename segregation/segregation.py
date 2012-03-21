# Nick Haliday
# Lab 14/15: Schelling's Segregation Model
# Torbert, period 1
# 2012-21-02


import random


def neighbors(r, c, rows, cols):
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            r_ = r + dr
            c_ = c + dc
            if 0 <= r_ < rows and 0 <= c_ < cols:
                yield r_, c_


class Population:
    
    X = 'X'
    O = 'O'
    BLANK = '.'
    DENSITY = 0.6

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
`       self.matrix = [[BLANK] * cols] * rows
        self.satisfied = False

        # populate the matrix
        numadd = int(DENSITY * rows * cols)
        while numadd:
            r = random.randrange(rows)
            c = random.randrange(cols)
            if self.matrix[r][c] != BLANK:
                continue
            else:
                self.matrix[r][c] = random.choice((X, O))
                numadd -= 1

    def shuffle():
        self.satisfied = True
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.satisfied(r, c):
                    self.satisfied = False
                    self.jiggle(r, c)

