#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# Romania, city dictionary builder

import sys
import json
import math
import collections

def main():
  with open('edge_list.txt') as adj, open('xy.txt') as dis, open('adjacency.json', 'w') as adjout, open('distance.json', 'w') as disout:
    edges = [l.split(',') for l in adj.read().split('\n')[:-1]]
    xy = [l.split(',') for l in dis.read().split('\n')[:-1]]
    loc = {l[0]: tuple(map(int, l[1:])) for l in xy}
    dis = collections.defaultdict(dict)
    for k1 in loc:
      for k2 in loc:
        dis[k1][k2] = math.hypot(loc[k1][0] - loc[k2][0], loc[k1][1] - loc[k2][1])
    neighbors = collections.defaultdict(list)
    for edge in edges:
      neighbors[edge[0]].append(edge[1])
      neighbors[edge[1]].append(edge[0])
    neighbors = {k: sorted(neighbors[k]) for k in neighbors}
    json.dump(neighbors, adjout, indent=4)
    json.dump(dis, disout, indent=4)


if __name__ == '__main__':
  main()

