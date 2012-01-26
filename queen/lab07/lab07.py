#!/usr/bin/env python3
# Nick Haliday, 10 November 2011
# Torbert, period 1
# N queens: Lab07


import random
import argparse
import bisect
import math
import copy
import time
import sys


### Utility ###

def show(board):
  print()
  for r in range(len(board)):
    s = ""
    for c in range(len(board)):
      if (r + c) % 2 == 1:
        s += chr(27) + "[31;46"
      else:
        s += chr(27) + "[31;43"
      s += "m"
      if board[c] == r:
        s += chr(27) + "[1m" + "X"
      else:
        s += " "
    print(chr(27) + "[0m" + s + chr(27) + "[0m")
  print(chr(27) + "[0m") 


def neighbors(perm):
  for i in range(len(perm)):
    for j in range(i + 1, len(perm)):
      yield (perm[:i] + (perm[j],) + perm[i + 1:j] + (perm[i],) +
          perm[j + 1:])


def pairs_attacking(perm):
  count = 0

  minors = [0 for i in range(2 * len(perm) - 1)]
  majors = [0 for i in range(2 * len(perm) - 1)]
  def minor(i, j):
    return i + j
  def major(i, j):
    return len(perm) - 1 + i - j
    
  for i in range(len(perm)):
    majors[major(i, perm[i])] += 1
    minors[minor(i, perm[i])] += 1
  for n in majors:
    count += n * (n - 1) // 2
  for n in minors:
    count += n * (n - 1) // 2

  appears = [0 for i in range(len(perm))]
  for i in perm:
    appears[i] += 1
  for n in appears:
    count += n * (n - 1) // 2

  return count


def is_solution(perm):
  return pairs_attacking(perm) == 0


def random_perm(n):
  def f():
    perm = list(range(n))
    random.shuffle(perm)
    return tuple(perm)
  return f


### Simulated Annealing ###

energ = {}
def energy(board):
  b = tuple(board)
  if b not in energ:
    energ[b] = pairs_attacking(b)
  return energ[b]


def log_schedule(initial=10**3):
  def f(i):
    return initial / math.log(i + 2)
  return f


def boltzmann(nxt, last, temperature):
  return math.exp(-1 / temperature * max(0, (nxt - last)))


def anneal(n, schedule=log_schedule()):
  x = random_perm(n)()
  i = 0
  while energy(x) > 0:
    nbrs = list(neighbors(x))
    e = energy(x)
    prob = [0]
    for n in nbrs:
      prob.append(prob[-1] + boltzmann(energy(n), e, schedule(i)))
    r = random.random() * prob[-1]
    for i, n in enumerate(nbrs):
      if r < prob[i + 1]:
        x = n
        break
    i = i + 1
  return True, x


### Hill Climb ###
h = {}
def heuristic(n):
  if n not in h:
    h[n] = pairs_attacking(n)
  return h[n]

def select_first(heuristic=heuristic):
  """Build a function that selects the first neighbors with a lower
  heuristic valuation"""
  def f(x, nbrs):
    nxt = x
    for n in nbrs:
      if heuristic(n) < heuristic(x):
        nxt = n
        break
      if heuristic(n) < heuristic(nxt):
        nxt = n
    return nxt
  return f


def select_min(heuristic=heuristic):
  """Build a function that chooses the neighbor with minimum heuristic
  valuation"""
  def f(x, nbrs):
    return min(nbrs, key=heuristic)
  return f


def select_weighted(heuristic=heuristic):
  """Build a function that chooses randomly but weights neighbors using
  the heuristic"""
  def f(x, nbrs):
    h0 = heuristic(x)
    nbrs = list(nbrs)
    h = [heuristic(n) for n in nbrs]
    psum = [0.0 for i in range(len(nbrs) + 1)]
    improv = [h0 - h[i] for i in range(len(nbrs))]
    lo = min(improv)
    improv = [v + lo for v in improv]
    total = sum(improv)
    if total == 0:
      return x
    for i, n in enumerate(nbrs):
      psum[i + 1] = psum[i] + improv[i] / total
    r = random.random()
    for i, v in enumerate(psum):
      if r >= v:
        return nbrs[i]
  return f


def hill_climb(x0, heuristic=heuristic, neighbors=neighbors,
    is_solution=is_solution, select=None, plateau=False):
  """A general hill climb"""
  if select is None:
    select = select_min(heuristic=heuristic)

  x = x0
  if plateau:
    vis = set()
    vis.add(x)

  while not is_solution(x):
    nbrs = neighbors(x)
    nxt = select(x, nbrs)
    if heuristic(x) > heuristic(nxt) or plateau and nxt not in vis:
      x = nxt
      if plateau:
        vis.add(x)
    else:
      return False, x

  return True, x


def simple(x0, heuristic=heuristic, neighbors=neighbors,
    is_solution=is_solution):
  """Run a first choice hill climb"""
  return hill_climb(x0, heuristic=heuristic,
      select=select_first(heuristic=heuristic))


def steepest(x0, heuristic=heuristic, neighbors=neighbors,
    is_solution=is_solution):
  """Run a steepest ascent hill climb"""
  return hill_climb(x0, heuristic=heuristic,
      select=select_min(heuristic=heuristic))


def plateau(x0, heuristic=heuristic, neighbors=neighbors,
    is_solution=is_solution):
  """Run a steepest ascent hill climb allowing plateaus"""
  return hill_climb(x0, heuristic=heuristic,
      select=select_min(heuristic=heuristic), plateau=True)

def stochastic(x0, heuristic=heuristic, neighbors=neighbors,
    is_solution=is_solution):
  """Do a weighted, randomized hill climb"""
  return hill_climb(x0, heuristic=heuristic,
      select=select_weighted(heuristic=heuristic))


def random_restart(n, retry=100, method=steepest,
    heuristic=heuristic, initial=None,
    neighbors=neighbors, is_solution=is_solution):
  """Run a random restart search"""
  if initial is None:
    initial = random_perm(n)

  h = {}
  def heur(nbr):
    nbr = tuple(nbr)
    if nbr not in h:
      h[nbr] = heuristic(nbr)
    return h[nbr]

  x0 = initial()
  minx = x0
  for i in range(retry):
    success, x = method(x0, heuristic=heur, neighbors=neighbors,
        is_solution=lambda b: heur(b) == 0)
    minx = min(minx, x, key=heur)
    if success:
      return True, minx
    x0 = initial()
  return False, minx


### Genetic Algorithm ###

fit = {}
def fitness(chromosome):
  b = tuple(chromosome.board)
  if b not in fit:
    fit[b] = -pairs_attacking(b)
  return fit[b]


class Chromosome:
  def __init__(self, n, board=None):
    self.n = n
    self.board = list(random_perm(n)()) if board is None else board

  def shuffle(self):
    random.shuffle(self.board)

  def __repr__(self):
    return repr(self.board)

  def __len__(self):
    return len(self.board)

  def __getitem__(self, key):
    return self.board[key]

  def __setitem__(self, key, val):
    self.board[key] = val

  def __iter__(self):
    return iter(self.board)

  def __lt__(self, chrom):
    return fitness(self) > fitness(chrom)

  def __copy__(self):
    return Chromosome(self.n, self.board)

  def __deepcopy__(self, memo):
    return Chromosome(self.n, copy.deepcopy(self.board, memo))


def indexes(n, rate=None):
  if rate is None:
    rate = random.random()
  return random.sample(range(n), int(rate * n))


def crossover(board1, board2, rate=None):
  newchrom1 = copy.deepcopy(board1)
  newchrom2 = copy.deepcopy(board2)
  n = min(board1.n, board2.n)
  for i in indexes(n, rate):
    newchrom1[i], newchrom2[i] = newchrom2[i], newchrom1[i]
  return newchrom1, newchrom2


def mutate(board, rate=None):
  newchrom = copy.deepcopy(board)
  for i in indexes(board.n, rate):
    newchrom[i] = random.randrange(board.n)
  return newchrom


def genetic(n, popsize=None, rate=0.5):
  if popsize is None:
    popsize = 2 * n
  if rate is None:
    rate = random.random()
  m = int(rate * popsize)

  population = []
  for i in range(popsize):
    population.append(Chromosome(n))
  population.sort()

  generations = 0
  while not is_solution(population[0]):
    del population[-m:]
    for i in range(math.floor(m / 2) if len(population) > 1 else 0):
      j = int(random.triangular(0, len(population) - 1, 0))
      k = int(random.triangular(j + 1, len(population), j + 1))
      # triangular distribution is biased toward low end
      chrom1, chrom2 = crossover(population[j], population[k])
      bisect.insort(population, chrom1)
      bisect.insort(population, chrom2)
    for i in range(math.ceil(m / 2) if len(population) > 1 else m):
      j = int(random.triangular(0, len(population), 0))
      bisect.insort(population, mutate(population[j]))
    generations += 1

  return True, population[0]


def main():
  n = int(sys.argv[1])
  annealc = 0
  annealt = []

  genc = 0
  gent = []

  hillc = 0
  hillt = []
  for i in range(1000):
    tic = time.time()
    success, _ = anneal(n)
    toc = time.time()
    annealc += success
    annealt.append(toc - tic)
  print(annealc / 1000, sum(annealt) / 1000)

  for i in range(20):
    tic = time.time()
    success, _ = steepest(random_perm(n)())
    toc = time.time()
    hillc += success
    hillt.append(toc - tic)
  print(hillc / 20, sum(hillt) / 20)

  for i in range(5):
    tic = time.time()
    success, _ = genetic(n)
    toc = time.time()
    genc += success
    gent.append(toc - tic)
  print(genc / 5, sum(gent) / 5)


if __name__ == "__main__":
  main()
