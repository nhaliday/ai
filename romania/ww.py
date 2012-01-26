#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# Waterway dictionary builder 

import sys
import json
import math
import collections

def main():
  with open('ww.txt') as fin, open('ww_location.json', 'w') as locout, open('ww_adjacency.json', 'w') as adjout:
    data = fin.read().split('\n')[:-1]
    n = int(data[0])
    m = int(data[n + 1])
    
    loc = {int(l[0]): tuple(map(float, l[1:3])) for l in (line.split() for line in data[1:1 + n])}
    edges = (tuple(map(int, l[:2])) for l in (line.split() for line in data[1 + n + 1:1 + n + 1 + m]))
    neighbors = collections.defaultdict(dict)
    for edge in edges:
      wht = math.hypot(loc[edge[0]][0] - loc[edge[1]][0], loc[edge[0]][1] - loc[edge[1]][1])
      neighbors[edge[0]][edge[1]] = wht
      neighbors[edge[1]][edge[0]] = wht

    json.dump(neighbors, adjout, indent=4, sort_keys=True)
    json.dump(loc, locout, indent=4)


if __name__ == '__main__':
  main()

