#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# AI: Lab 17 - Sudoku Solver


import sys
from pprint import pprint


VALS = set(range(1, 10))


### Backtracking ###


def has_k(A, i, j, k):
    i_ = i // 3
    j_ = j // 3
    for n in range(3 * i_, 3 * (i_ + 1)):
        for m in range(3 * j_, 3 * (j_ + 1)):
            if A[n][m] == k:
                return True
    return False


def find_blank(A):
    i = 0
    j = 0
    while A[i][j] != 0:
        if j < 8:
            j += 1
        elif i < 8:
            j = 0
            i += 1
        else:
            break
    return i, j


def recur(A, i, j):
    if A[i][j] != 0:
        return True

    collide = []
    for k in range(9):
        if A[i][k] != 0:
            collide.append(A[i][k])
        if A[k][j] != 0:
            collide.append(A[k][j])
    collide = set(collide)

    if len(collide) == 9:
        return False

    old = A[i][j]

    for k in VALS - collide:
        if not has_k(A, i, j, k):
            A[i][j] = k
            i_, j_ = find_blank(A)
            if recur(A, i_, j_):
                return True

    A[i][j] = old

    return False


def trans(puzz, blank='.'):
    A = [[0 for j in range(9)] for i in range(9)]
    for i, ch in enumerate(puzz):
        if ch != blank:
            r, c = divmod(i, 9)
            A[r][c] = int(ch)
    return A


def solve_backtrack(A):
    i, j = find_blank(A)
    return recur(A, i, j)


### END BACKTRACKING


def main():
    puzz = sys.argv[1]
    A = trans(puzz)
    pprint(A)
    pprint(solve_backtrack(A))
    pprint(A)


if __name__ == "__main__":
    main()
