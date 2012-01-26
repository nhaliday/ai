#!/usr/bin/env python3

import os, sys
import string
import collections

def main():
  with open(sys.argv[1]) as fin:
    freq = collections.defaultdict(int)
    for line in fin:
      word = line.lower().rstrip()
      for ch in word:
        freq[ch] += 1
    for ch in string.ascii_lowercase:
      print(ch, ': ', freq[ch], sep='')

if __name__ == "__main__":
  main()

