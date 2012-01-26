#!/usr/bin/env python3
# Nick Haliday, 13 September 2011
# Torbert, period 1
# Word Ladders: Lab02

import os
import sys
import random
import collections

def hamming(w1, w2):
  return sum(w1[i] != w2[i] for i in range(min(len(w1), len(w2)))) + abs(len(w1) - len(w2))

def neighbors(word, words):
  ws = []
  for w in words:
    if hamming(word, w) == 1:
      ws.append(w)
  return ws

def dfs(source, word, vis, path, adj, words):
  if word not in adj:
    adj[word] = neighbors(word, words)
  ns = adj[word]
  random.shuffle(ns)
  for w in ns:
    if not vis[w]:
      path[word] = w
      if hamming(source, w) == len(source) or dfs(source, w, vis, path, adj, words):
        return True
  return False

def main():
  with open(sys.argv[2]) as fin, open('lab02.out', 'w') as fout:
    source = sys.argv[1]
    words = fin.read().split()
    
    vis = collections.defaultdict(bool)
    path = {}
    adj = {}

    if dfs(source, source, vis, path, adj, words):
      w = source
      print(w, file=fout)
      while hamming(w, source) < len(source):
        print(w)
        w = path[w]
      print(w)
      print(w, file=fout)
    else:
      print('NO MATCH')

if __name__ == "__main__":
  main()

