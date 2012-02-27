#!/usr/bin/env python
# Nick Haliday
# Lab 11: Sobel Edge Detection
# 2012-01-24


import sys
import os
from os import path
import argparse

import scipy as sp
import numpy as np


GRAYSCALE = np.array([.30, .59, .11])


def grayscale(arr, gray=GRAYSCALE):
    return (arr[:, :, 0] * gray[0] + arr[:, :, 1] * gray[1] +
            arr[:, :, 2] * gray[2]).astype(np.int32)


def main():
    parser = argparse.ArgumentParser(description='detect edges in image')
    parser.add_argument('image', help='the image file')

    args = parser.parse_args()
    
    name, ext = os.path.splitext(args.image)
    with open(args.image) as fin, open(name + '.pgm', 'w') as fout:
        data = fin.read().split()

        M, N, scale = map(int, data[1:4])

        pixels = np.array(data[4:], dtype=np.int32)
        rgb = pixels.reshape(N, M, 3)
        gray = grayscale(rgb)
        sgray = gray.astype('|S{}'.format(len(str(scale))))

        print >>fout, 'P2'
        print >>fout, M, N
        print >>fout, scale
        print >>fout, ' '.join(sgray.flat)    


if __name__ == "__main__":
    main()
