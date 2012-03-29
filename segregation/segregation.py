# Nick Haliday
# Lab 14/15: Schelling's Segregation Model
# Torbert, period 1
# 2012-21-02


import random


def neighbors(r, c, rows, cols):
    for dr in range(-1, 1 + 1):
        for dc in range(-1, 1 + 1):
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
        self.allsatisfied = False

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

    def satisfied(self, r, c):
        if (0 <= r < self.rows and 0 <= c < self.cols and
                self.matrix[r][c] != Population.BLANK):
            n, m = 0, 0
            for r_, c_ in neighbors(r, c, self.rows, self.cols):
                if self.matrix[r_][c_] != BLANK:
                    n += 1
                if self.matrix[r_][c_] == self.matrix[r][c]:
                    m += 1
            if 1 <= n <= 3:
                return m >= 1
            elif 3 <= n < 6:
                return m >= 2
            elif 6 <= n:
                return m >= 3
        return True

    def displace(self, r, c):
        pass

    def shuffle():
        self.allsatisfied = True
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.satisfied(r, c):
                    self.allsatisfied = False
                    self.displace(r, c)

