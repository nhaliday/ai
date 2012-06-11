#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# AI: Lab 18 - Tic-Tac-Toe Learning


from itertools import *
import pickle


X = 0
O = 1
MAGIC = 12
R9 = set(range(9))


def win(moves):
    for i, j, k in combinations(moves, 3):
        if i + j + k == MAGIC:
            return True
    return False


def valid(currX, currO):
    if not currX | currO < R9:
        return False
    if currX & currO != set():
        return False
    if abs(len(currX) - len(currO)) >= 2:
        return False
    return True


def generate(turn=X, remaining=R9, currX=set(), currO=set()):
    if remaining and not win(currX) and not win(currO):
        yield (turn, frozenset(remaining), frozenset(currX), frozenset(currO))
        for i in remaining:
            if turn == X:
                for j in generate(O, remaining - {i}, currX | {i}, currO):
                    yield j
            else:
                for j in generate(X, remaining - {i}, currX, currO | {i}):
                    yield j


def possiblegames(game):
    turn, remaining, currX, currO = game
    for i in remaining:
        if turn == X:
            yield (turn, remaining - {i}, currX | {i}, currO)
        else:
            yield (turn, remaining - {i}, currX, currO | {i})


def xgames():
    return filter(lambda t: t[0] == X, generate())


def ogames():
    return filter(lambda t: t[0] == O, generate())


XGAMES = set(xgames())
OGAMES = set(ogames())
ALLGAMES = set(generate())


class RandomPlayer:

    def play(self, game):
        return random.choice(game[1])


class Learner:

    def __init__(self, matchbox):
        self.matchbox = matchbox
        self.history = []

    def play(self, game):
        for nextgame in possiblegames(game):
            pass
        

def main():

    xgames = None
    ogames = None

    try:
        with open('xmb.pickle') as xmb:
            xgames = pickle.load(xmb)
    except:
        xgames = dict(zip(XGAMES, repeat(0)))
    
    try:
        with open('omb.pickle') as omb:
            ogames = pickle.load(omb)
    except:
        ogames = dict(zip(OGAMES, repeat(0)))


