#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# AI: Lab 18 - Tic-Tac-Toe Learning


import itertools

X = 'X'
O = 'O'
MAGIC = 15


def win(moves):
    for i, j, k in itertools.combinations(moves, 3):
        if i + j + k == MAGIC:
            return moves
