#!/usr/bin/env python3

import os, sys

def main():
  with open(sys.argv[2]) as fin:
    target = sys.argv[1]
    flag = False
    for line in fin:
      word = line.lower().rstrip()
      if len(word) == len(target):
        n = 0
        for i in range(len(word)):
          if word[i] != target[i]:
            n += 1
            if n > 1:
              break
        if n == 1:
          flag = True
          print(word)
    if not flag:
      print('No words of the same length differed at exactly one position.')

if __name__ == "__main__":
  main()

