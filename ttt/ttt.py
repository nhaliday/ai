#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# AI: Lab 18 - Tic-Tac-Toe Learning


import random
import pickle
import copy

from pprint import pprint
from itertools import *


TRIALS = 20
X = 0
O = 1
XS = 'X'
OS = 'O'
R9 = frozenset(range(9))
INIT = (X, R9, frozenset(), frozenset())
### Magic! lol ###
MAGIC = 12
MAGICSQ = [[7, 0, 5],
           [2, 4, 6],
           [3, 8, 1]]
DB = "mb.pickle"
WT = 10


def translate(currX, currO):
    board = copy.deepcopy(MAGICSQ)
    for r in range(3):
        for c in range(3):
            if board[r][c] in currX:
                board[r][c] = X
            elif board[r][c] in currO:
                board[r][c] = O
            else:
                board[r][c] = None
    return board


def explicit(game):
    turn, remaining, currX, currO = game
    return (turn, translate(currX, currO))


def prettify(board):
    s = "+-" * 3 + "+\n"
    for r in range(3):
        for c in range(3):
            s += "|"
            if board[r][c] == X:
                s += XS
            elif board[r][c] == O:
                s += OS
            else:
                s += str(MAGICSQ[r][c])
        s += "|\n"

        s += "+-" * 3 + "+"
        if r != 2:
            s += '\n'
    return s


def unexplicit(explicit_game):
    turn, board = explicit_game
    remaining = frozenset()
    currX = frozenset()
    currO = frozenset()
    for r in range(3):
        for c in range(3):
            if board[r][c] == X:
                currX |= {MAGICSQ[r][c]}
            elif board[r][c] == O:
                currO |= {MAGICSQ[r][c]}
            else:
                remaining |= {MAGICSQ[r][c]}
    return (turn, remaining, currX, currO)


TWOPLAY = unexplicit((O, [[X, X, None],
                          [None, O, None],
                          [None, None, None]]))
BLOCK = unexplicit((X, [[X, X, O],
                        [None, O, None],
                        [None, None, None]]))


def win(moves):
    for i, j, k in combinations(moves, 3):
        if i + j + k == MAGIC:
            return True
    return False


def done(game):
    _, remaining, currX, currO = game
    return win(currX) or win(currO) or not remaining


def winner(game):
    _, _, currX, currO = game
    if win(currX):
        assert not win(currO)
        return X
    elif win(currO):
        return O
    else:
        return None


def move(i, game):
    turn, remaining, currX, currO = game
    if turn == X:
        return (O, remaining - {i}, currX | {i}, currO)
    else:
        return (X, remaining - {i}, currX, currO | {i})


def possiblegames(game):
    _, remaining, _, _ = game
    for i in remaining:
        yield move(i, game)


def generate(game=INIT):
    yield game
    if not done(game):
        for g in possiblegames(game):
            for j in generate(g):
                yield j


def xgames():
    return filter(lambda t: t[0] == X, generate())


def ogames():
    return filter(lambda t: t[0] == O, generate())


def play(xplayer, oplayer):
    game = INIT
    while not done(game):
        turn = game[0]
        oldgame = game
        if turn == X:
            game = xplayer.choose(game)
        else:
            game = oplayer.choose(game)
    w = winner(game)
    if w == X:
        xplayer.win()
        oplayer.lose()
    elif w == O:
        xplayer.lose()
        oplayer.win()
    else:
        xplayer.draw()
        oplayer.draw()


XGAMES = None
try:
    with open('xgames.pickle', 'rb') as xg:
        XGAMES = pickle.load(xg)
except:
    XGAMES = set(xgames())
    with open('xgames.pickle', 'wb') as xg:
        pickle.dump(XGAMES, xg)

OGAMES = None
try:
    with open('ogames.pickle', 'rb') as og:
        OGAMES = pickle.load(og)
except:
    OGAMES = set(ogames())
    with open('ogames.pickle', 'wb') as og:
        pickle.dump(OGAMES, og)

ALLGAMES = None
try:
    with open('allgames.pickle', 'rb') as ag:
        ALLGAMES = pickle.load(ag)
except:
    ALLGAMES = set(generate())
    with open('allgames.pickle', 'wb') as ag:
        pickle.dump(ALLGAMES, ag)


class Player:

    def choose(self, game):
        raise NotImplementedError

    def win(self):
        pass

    def draw(self):
        pass

    def lose(self):
        pass


class RandomPlayer(Player):

    def choose(self, game):
        return random.choice(list(possiblegames(game)))


class HeuristicPlayer(Player):

    def choose(self, game):
        turn, remaining, currX, currO = game
        for i in remaining:
            if win(currX | {i}) or win(currO | {i}):
                return move(i, game)
        return random.choice(list(possiblegames(game)))


class HumanPlayer(Player):
    
    def choose(self, game):
        turn, remaining, currX, currO = game
        print("turn:", XS if turn == X else OS)
        board = translate(currX, currO)
        print(prettify(board))
        print()

        i = int(input("Your move: "))

        newgame = move(i, game)
        _, _, currX, currO = newgame
        print(prettify(translate(currX, currO)))
        print()

        return newgame

    def win(self):
        print("YOU WIN!")

    def draw(self):
        print("YOU TIED.")

    def lose(self):
        print("YOU LOST...:(")


class LearnerPlayer(Player):

    def __init__(self, filename=DB):
        try:
            with open(filename, 'rb') as mbfile:
                self.matchbox = pickle.load(mbfile)
        except TypeError:
            if filename is None:
                filename = dict(zip(ALLGAMES, repeat(WT)))
            self.matchbox = filename
        except IOError:
            self.matchbox = dict(zip(ALLGAMES, repeat(WT)))
        self.history = []
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def choose(self, game):
        ngames = list(possiblegames(game))
        weights = [self.matchbox[ngame] for ngame in ngames]

        total = sum(weights)
        r = random.uniform(0, total)

        if not total:
            t = random.choice(ngames)
            self.history.append(t)
            return t

        _, oldremaining, _, _ = game

        w = 0

        choice = -1
        first = True
        for i, ngame in enumerate(ngames):
            w += weights[i]
            _, remaining, _, _ = ngame
            # print(tuple(oldremaining - remaining)[0], weights[i])
            if r < w and first:
                choice = i
                first = False
        self.history.append(ngames[choice])
        return ngames[choice]

        return None

    def win(self):
        for g in self.history:
            self.matchbox[g] += 2
            if self.matchbox[g] < WT:
                self.matchbox[g] = WT
        self.history = []
        self.wins += 1

    def draw(self):
        for g in self.history:
            self.matchbox[g] += 1
            if self.matchbox[g] < WT:
                self.matchbox[g] = WT
        self.history = []
        self.draws += 1

    def lose(self):
        for g in self.history:
            self.matchbox[g] -= 2
            if self.matchbox[g] < WT:
                self.matchbox[g] = WT
        self.history = []
        self.losses += 1

    def dump(self, filename=DB):
        with open(filename, 'wb') as fout:
            pickle.dump(self.matchbox, fout)


def main():
    learner = LearnerPlayer()
    driver = HumanPlayer()
    random = RandomPlayer()
    heuristic = HeuristicPlayer()

    gs = list(possiblegames(TWOPLAY))
    total = sum(map(lambda k: learner.matchbox[k], gs))
    print(learner.matchbox[BLOCK] / float(total))

    for i in range(TRIALS):
        play(driver, learner)

    learner.dump()

    print('{0.wins}-{0.draws}-{0.losses}'.format(learner))

if __name__ == "__main__":
    main()
