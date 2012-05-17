#!/usr/bin/env python3
# Nick Haliday
# Lab 16: Map Coloring


import copy
import random
from collections import defaultdict
from pprint import pprint


COLORS = {'RED', 'BLUE', 'GREEN', 'YELLOW'}


def check(adj, color):
    for k in adj:
        for v in adj[k]:
            if color[k] is not None:
                if color[k] == color[v]:
                    return False
    return True


def find(adj, possible, left):
    return min(left, key=lambda k: (len(possible[k]), -len(adj[k])))


def fourcolor_aux(adj, color, possible, left, target):
    for c in possible[target]:
        color[target] = c
        left.remove(target)
        leftaddback = set()
        possibleaddback = set()
        

        ok = True
        for n in adj[target]:
            if c not in left:
                if color[n] == color[target]:
                    ok = False
                    break
            else:
                if c in possible[n]:
                    possible[n].remove(c)
                    possibleaddback.add(n)

                    if not possible[n]:
                        ok = False
                        break
                
                    if len(possible) == 1:
                        left.remove(n)
                        leftaddback.add(n)

                        color[n] = tuple(possible[n])[0]


        if ok:
            if not left:
                return True

            nxt = find(adj, possible, left)
            if fourcolor_aux(adj, color, possible, left, nxt):
                return True

        for k in leftaddback:
            left.add(k)
        for k in possibleaddback:
            possible[k].add(c)

        left.add(target)
        color[target] = None

    return False


def fourcolor(adj):
    color = {k: None for k in adj}
    possible = {k: COLORS for k in adj}

    vertices = set(adj.keys())
    found = fourcolor_aux(adj, color, possible, vertices,
            random.choice(list(vertices)))

    return found, color


def trans(s):
    adj = defaultdict(set)
    for line in s.split('\n')[:-1]:
        a, b = line.split()
        adj[a].add(b)
        adj[b].add(a)
    return adj


def main():
    with open('states_48.txt') as fin:
        adj = trans(fin.read())
        sol, color = fourcolor(adj)
        pprint(sol)
        pprint(color)
        pprint(check(adj, color))


if __name__ == "__main__":
    main()
