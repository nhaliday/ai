#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# AI: Lab 18 - Tic-Tac-Toe Learning


import itertools

X = 'X'
O = 'O'
MAGIC = 12
R9 = set(range(9))


def win(moves):
    for i, j, k in itertools.combinations(moves, 3):
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


def extract(i):
    j = 0
    currX = set()
    currO = set()
    while j < 9:
        print(i, i % 3)
        if i % 3 == 1:
            currX.add(j)
        elif i % 3 == 2:
            currO.add(j)
        i //= 3
        j += 1
    print()
    return frozenset(currX), frozenset(currO)


# b = set()
# for i in range(3 ** 9):
#     currX, currO = extract(i)
#     if (valid(currX, currO) and not win(currX) and not win(currO) and
#             len(R9 - currX - currO) > 1):
#         b.add((currX, currO))
# print(len(b))


def generate(turn=X, remaining=R9, currX=set(), currO=set()):
    if len(remaining) > 1 and not win(currX) and not win(currO):
        yield (frozenset(currX), frozenset(currO))
        for i in remaining:
            if turn == X:
                for j in generate(O, remaining - {i}, currX | {i}, currO):
                    yield j
            else:
                for j in generate(X, remaining - {i}, currX, currO | {i}):
                    yield j


boards = set(generate())
s = set()
for currX, currO in boards:
    print(currX, currO)
    print(len(currX), len(currO), 9 - len(currX | currO))
    print()
print(len(boards))
