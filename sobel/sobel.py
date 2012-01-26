#!/usr/bin/env python3
# Nick Haliday
# Lab 11: Sobel Edge Detection
# 2012-01-24


import sys
import os
from os import path
import argparse

from math import *
from itertools import *


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def grayscale(r, g, b):
    return int(round(0.30*r + 0.59*g + 0.11*b))


def main():
    parser = argparse.ArgumentParser(description='detect edges in image')
    parser.add_argument('image', help='the image file')

    args = parser.parse_args()
    
    name, ext = os.path.splitext(args.image)
    assert(ext == '.ppm')
    with open(args.image) as fin, open(name + '.pgm', 'w') as fout:
        data = fin.read().split()
        assert(data[0] == 'P3')

        M, N = map(int, data[1:3])
        scale = int(data[3])

        pixels = map(int, data[4:])

        rgb = grouper(3, pixels)
        gray = starmap(grayscale, rgb)
        lines = grouper(M, map(str, gray))

        print('P2', file=fout)
        print(M, N, file=fout)
        print(scale, file=fout)
        for line in lines:
            print(' '.join(line), file=fout)


if __name__ == "__main__":
    main()
