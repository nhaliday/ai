# Nick Haliday
# Lab 14/15: Schelling's Segregation Model
# Torbert, period 1
# 2012-21-02


import random
import math
import copy
import pprint


X = 'X'
O = 'O'
BLANK = ' '


def neighbors(r, c, rows, cols):
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            r_ = r + dr
            c_ = c + dc
            if 0 <= r_ < rows and 0 <= c_ < cols and (r_, c_) != (r, c):
                yield r_, c_


class Population:

    def __init__(self, rows, cols, density=0.5):
        self.rows = rows
        self.cols = cols
        self.matrix = [[BLANK] * cols for i in range(rows)]
        self.steps = 0
        self.population = int(density * rows * cols)

        # populate the matrix
        numadd = self.population
        while numadd:
            r = random.randrange(rows)
            c = random.randrange(cols)
            if self.matrix[r][c] != BLANK:
                continue
            else:
                self.matrix[r][c] = random.choice((X, O))
                numadd -= 1

    def satisfied(self, r, c):
        if self.matrix[r][c] != BLANK:
            n, m = 0, 0
            for r_, c_ in neighbors(r, c, self.rows, self.cols):
                if self.matrix[r_][c_] != BLANK:
                    n += 1
                if self.matrix[r_][c_] == self.matrix[r][c]:
                    m += 1
            return 2 * m > n
        return True

    def better(self, r, c):
        for r_ in range(self.rows):
            for c_ in range(self.cols):
                if self.matrix[r_][c_] == BLANK:
                    self.matrix[r_][c_] = self.matrix[r][c]
                    self.matrix[r][c] = BLANK
                    ok = self.satisfied(r_, c_)
                    self.matrix[r][c] = self.matrix[r_][c_]
                    self.matrix[r_][c_] = BLANK
                    if ok:
                        yield r_, c_

    def best(self, r, c):
        minr, minc, d = -1, -1, float('inf')
        for r_, c_ in self.better(r, c):
            d_ = math.hypot(r_ - r, c_ - c)
            if d_ < d:
                minr, minc, d = r_, c_, d_
        return minr, minc


    def shuffle(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.satisfied(r, c):
                    r_, c_ = self.best(r, c)
                    if (r_, c_) == (-1, -1):
                        continue
                    self.matrix[r_][c_] = self.matrix[r][c]
                    self.matrix[r][c] = BLANK
                    self.steps += 1


    def allsatisfied(self):
        return all(self.satisfied(r, c) for r in range(self.rows) for
                c in range(self.cols))

    
    def segregated(self, r, c):
        for r_, c_ in neighbors(r, c, self.rows, self.cols):
            if self.matrix[r_][c_] != self.matrix[r][c]:
                return False
        return True


    def numsegregated(self):
        c = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.segregated(r, c):
                    c += 1
        return c


    def __str__(self):
        return '\n'.join(''.join(self.matrix[r][c] for c in
            range(self.cols)) for r in range(self.rows))


def main():
    x = range(5, 30)
    steps = []
    nseg = []

    for n in x:
        p = Population(n, n, .5)
        while not p.allsatisfied():
            p.shuffle()
        steps.append(p.steps)
        nseg.append(p.numsegregated())

    print zip(x, steps, nseg)
        

if __name__ == "__main__":
    main()
