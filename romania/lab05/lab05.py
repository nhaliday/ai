#!/usr/bin/env python3
# Nick Haliday, 4 October 2011
# Torbert, period 1
# Romania: Lab05

import sys
import json
import collections
import heapq
import argparse
import time

def dfs(source, target, neighbors, distances, lim=float('inf')):
  st = collections.deque()
  dis = {}      # stores lengths to avoid error in dfsid 
  previous = {} # stores pointer to previous node in path
  more = False  # stores whether we still have more nodes in the graph

  st.append((0, 0, (None, source))) # (distance, length in edges, (last node, currrent node))
  dis[source] = 0
  while st:
    dist, l, (last, node) = st.pop()
    if node == target:
      return True, more, previous, dist
    for n in neighbors[node]:
      if n not in dis or l + 1 < dis[n]:
        if l >= lim:
          more = True
          break
        st.append((dist + distances[node][n], l + 1, (node, n)))
        previous[n] = node
        dis[n] = l + 1

  return False, more, previous, float('inf')

def bfs(source, target, neighbors, distances, lim=float('inf')):
    q = collections.deque()
    vis = set()
    previous = {}
    more = False

    q.append((0, 0, (None, source)))
    vis.add(source)
    while q:
      dist, l, (last, node) = q.popleft()
      vis.add(node)
      if node == target:
        return True, more, previous, dist
      for n in neighbors[node]:
        if n not in vis:
          if l >= lim:
            more = True
            break
          q.append((dist + distances[node][n], l + 1, (node, n)))
          previous[n] = node

    return False, more, previous, float('inf')

def dfsid(source, target, neighbors, distances, lim=float('inf')):
  l = 0
  found, more, previous, dist = False, True, {}, float('inf')
  while l <= lim and not found and more:
    found, more, previous, dist = dfs(source, target, neighbors, distances, l)
    l += 1

  return found, more, previous, dist

def uni(source, target, neighbors, distances, lim=float('inf')):
  q = []
  vis = set()
  previous = {}
  more = False

  heapq.heappush(q, (0, 0, (None, source)))
  vis.add(source)
  while q:
    dist, l, (last, node) = heapq.heappop(q)
    vis.add(node)
    if node == target:
      return True, more, previous, dist
    for n in neighbors[node]:
      if n not in vis:
        if l >= lim:
          more = True
          break
        heapq.heappush(q, (dist + distances[node][n], l + 1, (node, n)))
        previous[n] = node

  return False, more, previous, float('inf')

def astar(source, target, neighbors, distances, lim=float('inf'), heuristic=None):
  q = []
  vis = set()
  previous = {}
  more = False
  if heuristic is None:
    heuristic = lambda n: distances[n][target]

  dist = collections.defaultdict(lambda: float('inf'))
  prior = {}
  dist[source] = 0
  prior[source] = dist[source] + heuristic(source)
  heapq.heappush(q, (prior[source], dist[source], 0, (None, source)))
  vis.add(source)
  while q:
    _, g, l, (last, node) = heapq.heappop(q) # prior is only for ordering so we don't need it here
    vis.add(node)
    if node == target:
      return True, more, previous, g
    for n in neighbors[node]:
      if n not in vis:
        if l >= lim:
          more = True
          break
      g_ = g + distances[node][n]
      if g_ < dist[n]:
        dist[n] = g_
        prior[n] = dist[n] + heuristic(n)
        heapq.heappush(q, (prior[n], dist[n], l + 1, (node, n)))
        previous[n] = node

  return False, more, previous, float('inf')

def walk(source, target, previous): # walk the path backwards, storing forwards
  p = collections.deque()
  node = target
  p.appendleft(node)
  while node != source:
    node = previous[node]
    p.appendleft(node)
  return p

def main():
  parser = argparse.ArgumentParser(description='Finds path from source word to target word.')
  parser.add_argument('source', metavar='S', help='the source word')
  parser.add_argument('target', metavar='T', help='the target word')
  parser.add_argument('-p', dest='print_path', action='store_true', help='print the path(s)')
  parser.add_argument('-m', '--method', nargs='+', choices={'bfs', 'dfs', 'dfsid', 'uni', 'astar'}, help='the method(s) to use for the search')
  parser.add_argument('-t', dest='time_run', action='store_true', help='track the time used for each search')
  parser.add_argument('-a', '--adj', help='the json adjacency dictionary to use', default='../adjacency.json')
  parser.add_argument('-d', '--dist', help='the json distance dictionary to use', default='../distance.json')
  args = parser.parse_args()

  with open(args.adj) as adj, open(args.dist) as dist:
    neighbors = json.load(adj)
    distances = json.load(dist)
    for name in args.method:
      tic = time.time()
      found, _, previous, length = globals()[name](args.source, args.target, neighbors, distances) # sketchy but easy
      toc = time.time()
      print(name.upper(), ':', sep='')
      if found:
        p = walk(args.source, args.target, previous)
        if args.print_path:
          for n in p:
            print(n)
        print('Length of path:', length)
        if args.time_run:
          print('Time taken:', toc - tic, 's')
      else:
        print('NO MATCH')

if __name__ == '__main__':
  main()
