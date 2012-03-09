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
from scipy import ndimage

from PIL import Image

GRAYSCALE = np.array([.30, .59, .11])
SMOOTH = np.array([[1.0, 2.0, 1.0],
                   [2.0, 4.0, 2.0],
                   [1.0, 2.0, 1.0]])
SMOOTH /= np.sum(SMOOTH)
GX = np.array([[1, 0, -1],
               [2, 0, -2],
               [1, 0, -1]])
GY = np.array([[-1, -2, -1],
               [0, 0, 0],
               [1, 2, 1]])
HIGH = 23
LOW = 16

def grayscale(arr):
    return (arr[:, :, 0] * GRAYSCALE[0] + arr[:, :, 1] * GRAYSCALE[1] +
            arr[:, :, 2] * GRAYSCALE[2]).astype(int)


def smooth(arr):
    return ndimage.convolve(arr, SMOOTH, mode='nearest')


def gradientx(arr):
    return ndimage.convolve(arr, GX, mode='nearest')


def gradienty(arr):
    return ndimage.convolve(arr, GY, mode='nearest')


def magnitude(gx, gy):
    return np.hypot(gx, gy)


def theta(gx, gy):
    return np.arctan2(gy, gx)


def roundto45(deg):
    deg = np.int64(np.around(deg / 45) * 45)
    deg[deg == -180] = 180 # restrict to the proper domain
    return deg


def main():
    parser = argparse.ArgumentParser(description='detect edges in image')
    parser.add_argument('image', help='the image file')

    args = parser.parse_args()

    infile = args.image
    name, ext = path.splitext(args.image)

    im = Image.open(infile)
    pix = np.array(im)

    gray = grayscale(pix)
    proc = smooth(gray)

    gx = gradientx(proc)
    gy = gradienty(proc)

    g = magnitude(gx, gy)
    rad = theta(gx, gy)
    deg = roundto45(np.rad2deg(rad))

    grayim = Image.fromarray(np.uint8(gray), 'L')
    grayim.save(name + "-gray.pgm")

    smoothim = Image.fromarray(np.uint8(proc), 'L')
    smoothim.save(name + "-smoothed.pgm")

    low = g > LOW
    highidx = np.where(g > HIGH)

    edge = np.tile(False, proc.shape)


if __name__ == "__main__":
    main()
