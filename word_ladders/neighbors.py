#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# Word Ladders: Neighbor list builder

import sys
import json

def is_neighbor(w1, w2):
  if len(w1) != len(w2):
    return False
  n = 0
  for i in range(len(w1)):
    if w1[i] != w2[i]:
      n += 1
      if n > 1:
        return False
  return n == 1

def neighbors(word, dictionary):
  for w in dictionary:
    if is_neighbor(word, w):
      yield w

def main():
  with open(sys.argv[1]) as fin, open('neighbors.json', 'w') as fout:
    dictionary = fin.read().split()
    ns = {}
    for word in dictionary:
      ns[word] = list(neighbors(word, dictionary))
    json.dump(ns, fout, indent=4)

if __name__ == '__main__':
  main()

