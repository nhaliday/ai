#!/usr/bin/env python
# Nick Haliday
# Lab 11: Sobel Edge Detection
# 2012-01-24


import sys
import os
from os import path
import argparse

import scipy as sp


GRAYSCALE = sp.array([.30, .59, .11])


def grayscale(arr):
    return (arr[:, :, 0] * GRAYSCALE[0] + arr[:, :, 1] * GRAYSCALE[1] +
            arr[:, :, 2] * GRAYSCALE[2]).astype(sp.int32)


def main():
    parser = argparse.ArgumentParser(description='detect edges in image')
    parser.add_argument('image', help='the image file')

    args = parser.parse_args()
    
    name, ext = os.path.splitext(args.image)
    with open(args.image) as fin, open(name + '.pgm', 'w') as fout:
        data = fin.read().split()

        M, N, scale = map(int, data[1:4])

        pixels = sp.array(data[4:], dtype=sp.int32)
        rgb = pixels.reshape(N, M, 3)
        gray = grayscale(rgb)
        sgray = gray.astype('|S{}'.format(len(str(scale))))

        print >>fout, 'P2'
        print >>fout, M, N
        print >>fout, scale
        print >>fout, ' '.join(sgray.flat)    


if __name__ == "__main__":
    main()
