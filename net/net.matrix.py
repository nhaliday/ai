#!/usr/bin/env python


import math
import random
import numpy as np


INIT = 0.2
XOR = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
      ]


@np.vectorize
def sigmoid(y):
    return 1 / (1 + np.exp(-y))


@np.vectorize
def dsigmoid(z):
    return z * (1 - z) # z = sigmoid(y)


class NeuralNetwork:

    def __init__(self, nin, nhid, nout):
        self.nin = nin
        self.nhid = nhid
        self.nout = nout

        self.win = np.random.uniform(-INIT, INIT, (self.nhid, self.nin + 1))
        self.wout = np.random.uniform(-INIT, INIT, (self.nout, self.nhid + 1))

        # activation values
        self.ain = np.zeros(self.nin + 1)
        self.ahid = np.zeros(self.nhid + 1)
        self.aout = np.zeros(self.nout)

    def update(self, inputs):
        if len(inputs) != self.nin:
            raise ValueError('wrong number of inputs')

        self.ain = np.append(np.copy(inputs), [1])
        self.ahid = np.append(sigmoid(np.dot(self.win, self.ain)), [1])
        self.aout = sigmoid(np.dot(self.wout, self.ahid))

        return self.aout.copy()

    def backprop(self, targets, mu):
        if len(targets) != self.nout:
            raise ValueError('wrong number of targets')

        # output deltas first
        # partial E wrt v_k = sum w_jk z_j where a_k = sigmoid(v_k)
        odelta = (self.aout - targets) * dsigmoid(self.aout)
        hdelta = np.dot(odelta, self.wout)[:-1] * dsigmoid(self.ain[:-1])

        self.wout -= mu * np.outer(odelta, self.aout)
        self.win -= mu * np.outer(hdelta, self.ain)

        return 0.5 * np.linalg.norm(targets - self.aout)

    def test(self, patterns):
        for p in patterns:
            print p[0], '->', self.update(p[0]), 'vs.', p[1]

    def weights(self):
        print 'Input to hidden weights:'
        print self.win
        print
        print 'Hidden to output weights:'
        print self.wout

    def train(self, patterns, iterations=1000, mu=0.5):
        for i in range(iterations):
            err = 0.0
            for inputs, targets in patterns:
                self.update(inputs)
                err += self.backprop(targets, mu)
            if i % 100 == 0:
                self.weights()
                self.test(patterns)
                print 'error {0}'.format(err)


def main():
    patterns = XOR
    n = NeuralNetwork(2, 2, 1)
    n.train(patterns)


if __name__ == "__main__":
    main()
