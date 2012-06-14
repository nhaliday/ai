#!/usr/bin/env python


import math
import random
import sys

import numpy as np


INIT = 0.2
XOR = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0])
        ]
NEGATION = [
        ([0], [1]),
        ([1], [0])
        ]
with open("iris.txt") as data:
    IRIS = [[], [], []]
    for line in data:
        raw = line.split()
        inputs = map(float, raw[:4])
        species = int(raw[-1]) - 1
        outputs = [0, 0, 0]
        outputs[species] = 1
        IRIS[species].append((inputs, outputs))


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

        # this is very hacky, can probably be refactored
        if self.nhid:
            self.win = np.random.uniform(-INIT, INIT, (self.nhid, self.nin + 1))
            self.wout = np.random.uniform(-INIT, INIT, (self.nout, self.nhid + 1))
        else:
            self.wout = np.random.uniform(-INIT, INIT, (self.nout, self.nin + 1))

        # activation values
        self.ain = np.ones(self.nin + 1)
        if self.nhid:
            self.ahid = np.ones(self.nhid + 1)
        self.aout = np.ones(self.nout)

    def update(self, inputs):
        if len(inputs) != self.nin:
            raise ValueError('wrong number of inputs')

        for i in range(self.nin):
            self.ain[i] = inputs[i]

        for j in range(self.nhid):
            self.ahid[j] = sigmoid(np.dot(self.win[j], self.ain))

        for k in range(self.nout):
            if self.nhid:
                self.aout[k] = sigmoid(np.dot(self.wout[k], self.ahid))
            else:
                self.aout[k] = sigmoid(np.dot(self.wout[k], self.ain))

        return self.aout.copy()

    def backprop(self, targets, mu):
        if len(targets) != self.nout:
            raise ValueError('wrong number of targets')

        # output deltas first
        # partial E wrt v_k = sum w_jk z_j where a_k = sigmoid(v_k)
        # odelta = (self.aout - targets) * dsigmoid(self.aout)
        # hdelta = np.dot(odelta, self.wout)[:-1] * dsigmoid(self.ain[:-1])
        
        # matrix ops not working for some reason :(, I have a bug
        # time to be more straightforward

        odelta = np.zeros(self.nout)
        for k in range(self.nout):
            odelta[k] = (self.aout[k] - targets[k]) * dsigmoid(self.aout[k])

        for k, j in np.ndindex(self.wout.shape):
            if self.nhid:
                self.wout[k, j] -= mu * odelta[k] * self.ahid[j]
            else:
                self.wout[k, j] -= mu * odelta[k] * self.ain[j]


        if self.nhid:
            hdelta = np.zeros(self.nhid)
            for j in range(self.nhid):
                hdelta[j] = dsigmoid(self.ahid[j]) * np.dot(self.wout[:, j], odelta)

            for j, i in np.ndindex(self.win.shape):
                self.win[j, i] -= mu * hdelta[j] * self.ain[i]

        # self.wout -= mu * np.outer(odelta, self.aout)
        # self.win -= mu * np.outer(hdelta, self.ain)

        return 0.5 * np.linalg.norm(targets - self.aout)

    def test(self, patterns, stream=sys.stdout):
        for p in patterns:
            print >>stream,  p[0], '->', self.update(p[0]), 'vs.', p[1]

    def weights(self, stream=sys.stdout):
        if self.nhid:
            print >>stream, 'Input to hidden weights:'
            print >>stream, self.win
            print >>stream
            print >>stream, 'Hidden to output weights:'
            print >>stream, self.wout
        else:
            print >>stream, 'Input to output weights:'
            print >>stream, self.wout

    def train(self, patterns, iterations=1000, mu=0.5, log=True):
        self.errors = []
        for i in range(iterations):
            err = 0.0
            for inputs, targets in patterns:
                self.update(inputs)
                err += self.backprop(targets, mu)
            if log and i % 100 == 0:
                self.weights()
                self.test(patterns)
                print 'error {0}'.format(err)
            self.errors.append(err)


def main():
    neg = NeuralNetwork(1, 0, 1)
    neg.train(NEGATION, iterations=1000, mu=0.8, log=False)
    with open("neg.errors", 'w') as errfile, open("neg.test", 'w') as testfile:
        print >>errfile, neg.errors
        neg.test(NEGATION, testfile)

    xor = NeuralNetwork(2, 2, 1)
    xor.train(XOR, iterations=10000, mu=0.8, log=False)
    with open("xor.errors", 'w') as errfile, open("xor.test", 'w') as testfile:
       print >>errfile, xor.errors
       xor.test(XOR, testfile)

    iris = NeuralNetwork(4, 50, 3)
    for i in range(3):
        # train on the first half of each species then test on 2nd half
        n = len(IRIS[i])
        l = n / 2
        iris.train(IRIS[i][:l], iterations=100, mu=0.99, log=False)
        with open("iris.%d.errors" % i, 'w') as errfile, \
          open("iris.%d.test" % i, 'w') as testfile:
            print >>errfile, iris.errors
            iris.test(IRIS[i][l:], testfile)


if __name__ == "__main__":
    main()
