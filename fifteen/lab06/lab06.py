#!/usr/bin/env python3
# Nick Haliday, 25 October 2011
# Torbert, period 1
# Sliding tiles: Lab06

from tkinter import *
from tkinter import ttk
import os
import sys
import collections
import heapq
import random
import functools


def ncycles(f):
  ncycles = 0
  seen = collections.defaultdict(bool)
  for i in f:
    if not seen[i]:
      ncycles += 1
      j = i
      while not seen[f[j]]:
        j = f[j]
        seen[j] = True
  return ncycles


def parity(f):
  return (len(f) - ncycles(f)) % 2


class Position:
  def __init__(self, n=None, sigma=None):
    if n is None:
      n = 4
    self.n = n
    self.blank = n**2 - 1
    if sigma is None:
      sigma = tuple(range(n**2))
    if len(sigma) != n**2 or set(sigma) != set(range(n**2)):
      raise ValueError('bad permutation')
    self.sigma = sigma
    self.i = sigma.index(self.blank)

  def __eq__(self, other):
    return self.sigma == other.sigma

  def __lt__(self, other):
    return self.sigma < other.sigma

  def __hash__(self):
    return hash(self.sigma)

  def __len__(self):
    return len(self.sigma)

  def __getitem__(self, i):
    return self.sigma[i]

  def __iter__(self):
    return iter(self.sigma)

  def __repr__(self):
    return '\n'.join(repr(self.sigma[i:i + self.n]) for i in range(0, self.n**2, self.n))

  def right(self):
    n = self.n
    i = self.i
    sigma = self.sigma
    if (i + 1) % n != 0:
      sigma_ = sigma[:i] + (sigma[i + 1], sigma[i]) + sigma[i + 2:]
      return Position(n, sigma=sigma_)

  def up(self):
    n = self.n
    i = self.i
    sigma = self.sigma
    if i >= n:
      sigma_ = sigma[:i - n] + (sigma[i],) + sigma[i - n + 1:i] + (sigma[i - n],) + sigma[i + 1:]
      return Position(n, sigma=sigma_)

  def left(self):
    n = self.n
    i = self.i
    sigma = self.sigma
    if i % n != 0:
      sigma_ = sigma[:i - 1] + (sigma[i], sigma[i - 1]) + sigma[i + 1:]
      return Position(n, sigma=sigma_)

  def down(self):
    n = self.n
    i = self.i
    sigma = self.sigma
    if i < n*(n - 1):
      sigma_ = sigma[:i] + (sigma[i + n],) + sigma[i + 1:i + n] + (sigma[i],) + sigma[i + n + 1:]
      return Position(n, sigma=sigma_)

  def neighbors(self):
    for f in (self.right, self.up, self.left, self.down):
      res = f()
      if res is not None:
        yield res

  def shuffle(self):
    sigma_ = list(self.sigma)
    random.shuffle(sigma_)
    newpos = Position(self.n, sigma=tuple(sigma_))
    row, col = divmod(newpos.i, newpos.n)
    parity_manhattan = (row + col) % 2
    if parity_manhattan != parity(newpos):
      if newpos.i != 0 and newpos.i != 1:
        sigma_[0], sigma_[1] = sigma_[1], sigma_[0]
      else:
        sigma_[self.n], sigma_[self.n + 1] = sigma_[self.n + 1], sigma_[self.n]
    newpos = Position(self.n, sigma=tuple(sigma_))
    assert parity_manhattan == parity(newpos)
    return newpos


def manhattan(node):
  s = 0
  for i in range(node.n**2):
    if i != node.i:
      row, col = divmod(i, node.n)
      row_, col_ = divmod(node[i], node.n)
      s += abs(row - row_) + abs(col - col_)
  return s


def linear_conflict(node):
  s = 0
  for row in range(node.n):
    for col1 in range(node.n):
      i1 = row * node.n + col1
      if i1 != node.i:
        for col2 in range(col1 + 1, node.n):
          i2 = row * node.n + col2
          row1_, col1_ = divmod(node[i1], node.n)
          row2_, col2_ = divmod(node[i2], node.n)
          if row1_ == row == row2_ and col2_ < col1_:
            s += 2
  return s


def manhattan_linear_conflict(node):
  return manhattan(node) + linear_conflict(node)

# TODO: GET THIS WORKING!
def solve(src, heuristic=None):
  q = []
  vis = set()
  previous = {}
  if heuristic is None:
    heuristic = manhattan_linear_conflict
  target = Position(src.n)

  dist = collections.defaultdict(lambda: float('inf'))
  prior = {}
  dist[src] = 0
  prior[src] = dist[src] + heuristic(src)
  heapq.heappush(q, (prior[src], dist[src], src))
  vis.add(src)
  while q:
    _, g, node = heapq.heappop(q) # prior is only for ordering so we don't need it here
    vis.add(node)
    if node == target:
      return True, previous, g
    for i, n in enumerate(node.neighbors()):
      g_ = g + 1
      if n not in vis and g_ < dist[n]:
        dist[n] = g_
        prior[n] = dist[n] + heuristic(n)
        heapq.heappush(q, (prior[n], dist[n], n))
        if i == 0:   # right
          previous[n] = Position.left
        elif i == 1: # up
          previous[n] = Position.down
        elif i == 2: # left
          previous[n] = Position.right
        elif i == 3: # down
          previous[n] = Position.up

    return False, previous, float('inf')


class Application(ttk.Frame):
  def __init__(self, master=None, n=None, tile_width=100, tile_height=100):
    self.position = Position(n)
    self.n = self.position.n
    self.tile_bord = (20, 20)
    self.tile_dim = (tile_width, tile_height)
    self.canvas_dim = (2 * self.tile_bord[0] + self.n * self.tile_dim[0] + 500, 2 * self.tile_bord[1] + self.n * self.tile_dim[1])

    ttk.Frame.__init__(self, master, width=self.canvas_dim[0], height=self.canvas_dim[1])
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)
    self.grid()
    self.make_widgets()
    self.focus_set()
    
  def shuffle(self):
    self.position = self.position.shuffle()
    self.update()

  def make_widgets(self):
    self.canvas = Canvas(self, width=self.canvas_dim[0], height=self.canvas_dim[1], bg='white')
    self.canvas.grid()

    self.tile = []
    self.text = []
    
    for i in range(self.n**2):
      row, col = divmod(i, self.n)
      ix = self.tile_bord[0] + self.tile_dim[0] * col
      iy = self.tile_bord[1] + self.tile_dim[1] * row
      ex = ix + self.tile_dim[0]
      ey = iy + self.tile_dim[1]
      recid = self.canvas.create_rectangle((ix, iy, ex, ey), fill='orange')

      textid = self.canvas.create_text((ix + ex) / 2, (iy + ey) / 2)

      self.tile.append(recid)
      self.text.append(textid)

    self.canvas.bind('<Button-1>', lambda event: self.click(event))
    self.bind('s', lambda event: self.shuffle())

    self.par = self.canvas.create_text(2 * self.tile_bord[0] + self.n * self.tile_dim[0] + 250, 50)
    self.heur1 = self.canvas.create_text(2 * self.tile_bord[0] + self.n * self.tile_dim[0] + 250, 1/2 * self.canvas_dim[1])
    self.heur2 = self.canvas.create_text(2 * self.tile_bord[0] + self.n * self.tile_dim[0] + 250, self.canvas_dim[1] - 50)

    self.update()

  def click(self, event):
    x, y = event.x, event.y
    x -= self.tile_bord[0]
    y -= self.tile_bord[1]
    col = x // self.tile_dim[0]
    row = y // self.tile_dim[1]
    n = self.n
    if row < n and col < n:
      i = row * n + col
      if i - 1 == self.position.i:   # right
        self.right()
      elif i + n == self.position.i: # up
        self.up()
      elif i + 1 == self.position.i: # left
        self.left()
      elif i - n == self.position.i: # down
        self.down()

  def update(self):
    for i in range(self.n**2):
      if i == self.position.i:
        self.canvas.itemconfigure(self.text[i], text='')
      else:
        self.canvas.itemconfigure(self.text[i], text=repr(self.position[i] + 1))
    self.canvas.itemconfigure(self.par, text='Even' if parity(self.position) else 'Odd')
    self.canvas.itemconfigure(self.heur1, text=repr(manhattan(self.position)))
    self.canvas.itemconfigure(self.heur2, text=repr(manhattan_linear_conflict(self.position)))

  def right(self):
    newpos = self.position.right()
    if newpos is not None:
      self.position = newpos
    self.update()

  def up(self):
    newpos = self.position.up()
    if newpos is not None:
      self.position = newpos
    self.update()

  def left(self):
    newpos = self.position.left()
    if newpos is not None:
      self.position = newpos
    self.update()

  def down(self):
    newpos = self.position.down()
    if newpos is not None:
      self.position = newpos
    self.update()

    

def main():
  # sol = solve(Position().shuffle())
  # print(sol)
  root = Tk()
  app = Application(master=root, n=4)
  app.mainloop()


if __name__ == "__main__":
  main()

