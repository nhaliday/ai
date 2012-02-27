#!/usr/bin/env python
# Nick Haliday
# Lab 11/12: Canny Edge Detection
# 2012-02-21


import argparse
import numpy as np
import scipy as sp


SMOOTH = np.array([[1.0, 2.0, 1.0],
                   [2.0, 4.0, 2.0],
                   [1.0, 2.0, 1.0]])
SMOOTH /= np.linalg.norm(SMOOTH)

GX = np.array([[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]])

GY = np.array([[1, 2, 1]
               [0, 0, 0]
               [-1, -2, -1]])


def main():
    parser = argparse.ArgumentParser(description


if __name__ == "__main__":
    main()
