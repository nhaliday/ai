#!/usr/bin/env python3
# Nick Haliday, 13 September 2011
# Torbert, period 1
# Word Ladders: Lab01

import os
import sys

def main():
  with open(sys.argv[2]) as fin:
    target = sys.argv[1]
    isword = False
    neighbors = []
    for word in (line.lower().rstrip() for line in fin):
      if len(word) == len(target):
        n = 0
        for i in range(len(word)):
          if word[i] != target[i]:
            n += 1
            if n > 1:
              break
        if n == 0:
          isword = True
        if n == 1:
          neighbors.append(word)
    if not isword:
      print('NO SUCH WORD')
    elif not neighbors:
      print('NO MATCH')
    else:
      for n in neighbors:
        print(n)

if __name__ == "__main__":
  main()

