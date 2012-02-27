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
GAUSSIAN = sp.array([[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]])
GX = sp.array([[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]])
GY = sp.array([[1, 2, 1],
               [0, 0, 0],
               [-1, -2, -2]])


def grayscale(arr):
    return (arr[:, :, 0] * GRAYSCALE[0] + arr[:, :, 1] * GRAYSCALE[1] +
            arr[:, :, 2] * GRAYSCALE[2]).astype(sp.int32)

def apply(arr, mask):
    arr = sp.zeros(arr.shape)
    for row in range(1, arr.shape[0] - 1):
        for col in range(1, arr.shape[1] - 1):
            val = 0
            orig = (1, 1)
            for r in range(-1, 2):
                for c in range(-1, 2):
                    


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
