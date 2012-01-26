#!/usr/bin/env python
# Nick Haliday
# Lab 11: Sobel Edge Detection
# 2012-01-24


import sys
import os
from os import path
import argparse

import numpy as np

from itertools import *


def grayscale(rgb, g=None, b=None):
    if g is not None:
        rgb = [rgb, g, b]
    return int(round(0.30*rgb[0] + 0.59*rgb[1] + 0.11*rgb[2]))


def main():
    parser = argparse.ArgumentParser(description='detect edges in image')
    parser.add_argument('image', help='the image file')

    args = parser.parse_args()
    
    name, ext = os.path.splitext(args.image)
    with open(args.image) as fin, open(name + '.pgm', 'w') as fout:
        data = fin.read().split()

        M, N = map(int, data[1:3])
        scale = int(data[3])

        pixels = np.array(data[4:], dtype='int')
        rgb = pixels.reshape(N, M, 3)
        gray = np.apply_along_axis(grayscale, 2, rgb)

        print >>fout, 'P2'
        print >>fout, M, N
        print >>fout, scale
        print >>fout, ' '.join(map(str, gray.flat))    


if __name__ == "__main__":
    main()
