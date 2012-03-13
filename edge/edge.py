#!/usr/bin/env python
# Nick Haliday
# Lab 11: Sobel Edge Detection
# 2012-01-24


import sys
import os
from os import path
import argparse

import math
import scipy as sp
import numpy as np
from scipy import ndimage

from PIL import Image


GRAYSCALE = np.array([.30, .59, .11])
SMOOTH = np.array([[1.0, 2.0, 1.0],
                   [2.0, 4.0, 2.0],
                   [1.0, 2.0, 1.0]])
SMOOTH /= np.sum(SMOOTH)
GX = np.array([[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]])
GY = np.array([[1, 2, 1],
               [0, 0, 0],
               [-1, -2, -1]])

HIGH = 100
LOW = 50
MAXC = 256

BINHEIGHT = 15
BINWIDTH = 15


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
    # return np.abs(gx) + np.abs(gy)


def theta(gx, gy):
    return np.arctan2(gy, gx)


def roundto45(deg):
    deg = np.int64(np.around(deg / 45) * 45)
    deg %= 360 # restrict to the proper domain
    return deg


def forward(r, c, deg):
    if deg == 0:
        return (r, c + 1)
    elif deg == 45:
        return (r - 1, c + 1)
    elif deg == 90:
        return (r - 1, c)
    elif deg == 135:
        return (r - 1, c - 1)
    elif deg == 180:
        return (r, c - 1)
    elif deg == 225:
        return (r + 1, c - 1)
    elif deg == 270:
        return (r + 1, c)
    elif deg == 315:
        return (r + 1, c + 1)
    raise ValueError("requires deg == 0 (mod 45) and 0 <= deg < 360")


def neighbors(r, c, deg):
    return forward(r, c, deg), forward(r, c, (deg + 180) % 360)

def flood(r, c, low, high, deg, edge):
    N, M = low.shape
    if 0 <= r < N and 0 <= c < M and low[r, c] and not edge[r, c]:
        edge[r, c] = True
        forward = (deg[r, c] + 90) % 360
        (r1, c1), (r2, c2) = neighbors(r, c, deg[r, c])
        flood(r1, c1, low, high, deg, edge)
        flood(r2, c2, low, high, deg, edge)


def move(r0, c0, p, theta):
    return (r0 - p * np.sin(theta), c0 + p * np.cos(theta))


def bin(r, c):
    return (int(r) / BINHEIGHT, int(c) / BINWIDTH)


def main():
    parser = argparse.ArgumentParser(description='detect edges in image')
    parser.add_argument('image', help='the image file')

    args = parser.parse_args()

    infile = args.image
    name, ext = path.splitext(infile)

    im = Image.open(infile)
    pix = np.array(im)
    N, M, _ = pix.shape

    gray = grayscale(pix)
    smoothed = smooth(gray)
    proc = smoothed

    gx = gradientx(proc)
    gy = gradienty(proc)

    g = magnitude(gx, gy)
    rad = theta(gx, gy)
    deg = roundto45(np.rad2deg(rad))

    grayim = Image.fromarray(np.uint8(gray), 'L')
    grayim.save(name + "-gray.pgm")

    smoothim = Image.fromarray(np.uint8(smoothed), 'L')
    smoothim.save(name + "-smoothed.pgm")

    intensityim = Image.fromarray(np.uint8(g), 'L')
    intensityim.save(name + "-test.pgm")

    low = g > LOW
    high = g > HIGH
    highidx = np.where(high)

    edge = np.tile(False, proc.shape)

    for r, c in zip(*highidx):
        flood(r, c, low, high, deg, edge)

    edgeidx = np.where(edge)
    for r, c in zip(*edgeidx):
        (r1, c1), (r2, c2) = neighbors(r, c, deg[r, c])
        if 0 <= r1 < N and 0 <= c1 < M:
            if edge[r1, c1] and g[r1, c1] > g[r, c]:
                edge[r, c] = False
        if 0 <= r2 < N and 0 <= c2 < M:
            if edge[r2, c2] and g[r2, c2] > g[r, c]:
                edge[r, c] = False
    edgeidx = np.where(edge)

    nice = np.zeros(proc.shape + (3,))
    nice[:, :] = proc[:, :, np.newaxis]
    nice[edge] = [MAXC - 1, 0, 0]

    niceim = Image.fromarray(np.uint8(nice))
    niceim.save(name + "-detect.ppm")

    binN = (proc.shape[0] + BINHEIGHT - 1) / BINHEIGHT
    binM = (proc.shape[1] + BINWIDTH - 1) / BINWIDTH
    bins = np.zeros((binN, binM), dtype=int)
    for r0, c0 in zip(*edgeidx):
        for p in range(1, max(N, M), min(BINWIDTH, BINHEIGHT)):
            r, c = move(r0, c0, p, rad[r0, c0])
            rbin, cbin = bin(r, c)
            if 0 <= rbin < binN and 0 <= cbin < binM:
                bins[rbin, cbin] += 1
            else:
                break
    maxbin = np.max(bins)

    displaybin = maxbin - bins
    pixelated = np.repeat(np.repeat(displaybin * MAXC / maxbin, BINHEIGHT,
        0), BINWIDTH, 1)
    colored = np.zeros(pixelated.shape + (3,))
    colored[:, :] = pixelated[:, :, np.newaxis]
    colored[edge] = [255, 0, 0]
    pixelatedim = Image.fromarray(np.uint8(colored))
    pixelatedim.save(name + '-bin.ppm')


if __name__ == "__main__":
    main()
