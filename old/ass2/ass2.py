#!/usr/bin/env python3

import os, sys

def main():
  with open(sys.argv[2]) as fin:
    target = sys.argv[1]
    for i, line in enumerate(fin):
      word = line.lower().rstrip()
      if word == target:
        print('Yes, ', target, ' is at position ', i, '.', sep='')
        break
    else:
      print('No,', target, 'is not in the dictionary.')

if __name__ == "__main__":
  main()

