#!/usr/bin/env python3
# Nick Haliday, 22 September 2011
# Torbert, period 1
# Word Ladders: Lab03

import sys
import json
import collections
import argparse
import time

def dfs(source, target, neighbors, lim=float('inf')):
  st = collections.deque()
  dis = {}      # stores lengths to avoid error in dfsid 
  previous = {} # stores pointer to previous node in path
  more = False  # stores whether we still have more nodes in the graph

  st.append((None, source, 0)) # (lastNode, currNode, lengthOfPath)
  dis[source] = 0
  while len(st) > 0:
    last, node, l = st.pop()
    if node == target:
      return True, more, previous
    for n in neighbors[node]:
      if n not in dis or l + 1 < dis[n]:
        if l >= lim:
          more = True
          break
        st.append((node, n, l + 1))
        previous[n] = node
        dis[n] = l + 1

  return False, more, previous

def bfs(source, target, neighbors, lim=float('inf')):
    q = collections.deque()
    vis = set()
    previous = {}
    more = False

    q.append((None, source, 0))
    vis.add(source)
    while len(q) > 0:
      last, node, l = q.popleft()
      if node == target:
        return True, more, previous
      for n in neighbors[node]:
        if n not in vis:
          if l >= lim:
            more = True
            break
          q.append((node, n, l + 1))
          previous[n] = node
          vis.add(n)

    return False, more, previous

def dfsid(source, target, neighbors, lim=float('inf')):
  l = 0
  found, more, previous = False, True, {}
  while l <= lim and not found and more:
    found, more, previous = dfs(source, target, neighbors, l)
    l += 1

  return found, more, previous

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
  parser.add_argument('-m', '--method', nargs='+', choices={'bfs', 'dfs', 'dfsid'}, help='the method(s) to use for the search')
  parser.add_argument('-t', dest='time_run', action='store_true', help='track the time used for each search')
  parser.add_argument('-d', '--dict', help='the json dictionary to use', default='../neighbors.json')
  args = parser.parse_args()

  with open(args.dict) as fin:
    dictionary = json.load(fin)
    for name in args.method:
      tic = time.time()
      found, _, previous = globals()[name](args.source, args.target, dictionary) # sketchy but easy
      toc = time.time()
      print(name.upper(), ':', sep='')
      if found:
        p = walk(args.source, args.target, previous)
        if args.print_path:
          for n in p:
            print(n)
        print('Length of path:', len(p))
        if args.time_run:
          print('Time taken:', toc - tic, 's')
      else:
        print('NO MATCH')

if __name__ == '__main__':
  main()