#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# AI: Lab 17 - Sudoku Solver


import sys

from itertools import combinations, product
from copy import copy, deepcopy
from pprint import pprint
from collections import defaultdict


VALS = set(range(1, 10))

### neighbor list ###

ADJ = defaultdict(set)

def sq(i, j):
    return product(range(3 * i, 3 * (i + 1)), range(3 * j, 3 * (j + 1)))

for r in range(9):
    for c1, c2 in combinations(range(9), 2):
        ADJ[(r, c1)].add((r, c2))
        ADJ[(r, c2)].add((r, c1))

for c in range(9):
    for r1, r2 in combinations(range(9), 2):
        ADJ[(r1, c)].add((r2, c))
        ADJ[(r2, c)].add((r1, c))

for i in range(3):
    for j in range(3):
        for (r1, c1), (r2, c2) in combinations(sq(i, j), 2):
            ADJ[(r1, c1)].add((r2, c2))
            ADJ[(r2, c2)].add((r1, c1))

### done with that ###


def trans(puzz, blank='.'):
    A = [[0 for j in range(9)] for i in range(9)]
    for i, ch in enumerate(puzz):
        if ch != blank:
            r, c = divmod(i, 9)
            A[r][c] = int(ch)
    return A


def find_next(A, i, j, possible):
    def key(r_c):
        r, c = r_c
        return (len(possible[r][c]), -len(ADJ[(r, c)]))
    return min(((r, c) for r, c in ADJ if A[r][c] != 0), key=key)


def propagate(A, i, j, possible):
    for r, c in ADJ[(i, j)]:
        if A[r][c] == A[i][j]:
            return False
        possible[r][c].remove(A[i][j])
        if not possible[r][c]:
            return False
        if len(possible[r][c]) == 1:
            A[r][c] = tuple(possible[r][c])(0)
            if not propagate(A, r, c, possible):
                return False
    return True


def recur(A, i, j, possible):
    for v in possible[i][j]:
        Ac = deepcopy(A)
        possiblec = deepcopy(possible)

        Ac[i][j] = v
        if not propagate(Ac, i, j, possiblec):
            return

        try:
            r, c = find_next(Ac, possiblec)
        except:
            yield Ac
            return

        for solution in recur(Ac, r, c, possible):
            yield solution


def solve(A):
    possible = [[VALS for j in range(9)] for i in range(9)]
    for i in range(9):
        for j in range(9):
            if A[i][j] != 0:
                possible[i][j] = [A[i][j]]
                if not propagate(A, i, j, possible):
                    return
    i, j = find_blank(A, possible)
    for solution in recur(A, i, j, possible):
        yield solution


def main():
    pprint(ADJ)

    puzz = sys.argv[1]
    A = trans(puzz)
    pprint(A)
    for sol in solve(A):
        pprint(sol)
    pprint(A)


if __name__ == "__main__":
    main()
