#!/usr/bin/env python3
# Nick Haliday, 25 October 2011
# Torbert, period 1
# Sliding tiles: Lab06

from tkinter import *
from tkinter.ttk import *
import os
import sys
import collections
import random


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
  return (len(f) - ncycles(f)) % 2 == 0


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

  def __hash__(self):
    return hash(self.sigma)

  def __len__(self):
    return len(self.sigma)

  def __getitem__(self, i):
    return self.sigma[i]

  def __iter__(self):
    return iter(self.sigma)

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
    for f in {self.right, self.up, self.left, self.down}:
      res = f()
      if res is not None:
        yield res

  def shuffle(self):
    sigma_ = list(self.sigma)
    random.shuffle(sigma_)
    if not parity(sigma_):
      sigma_[0], sigma_[1] = sigma_[1], sigma_[0]
    sigma_ = tuple(sigma_)
    return Position(self.n, sigma=sigma_)


class Application(Frame):
  def __init__(self, master=None, n=None):
    Frame.__init__(self, master)
    self.position = Position(n)
    self.n = self.position.n
    self.grid()
    self.style()
    self.make_widgets()
    
  def shuffle(self):
    self.position = self.position.shuffle()
    self.update()

  def style(self):
    self.style = Style()
    self.style.configure('T.TLabel', fg='red', bg='black')
    self.style.configure('T.TButton', relief='raised', fg='red', bg='black', borderwidth=5)

  def make_widgets(self):
    self.label = Label(self, text='Sliding Tile Puzzle', style='T.TLabel') 
    self.label.grid(row=0, columnspan=self.n, sticky='nesw')

    self.board = []
    for i in range(self.n**2):
      self.board.append(Button(self, style='T.TButton'))
      row, col = divmod(i, self.n)
      self.board[i].grid(row=1 + row, column=col, sticky='nesw') 
    self.update()

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

  def update(self):
    for i in range(self.n**2):
      if i == self.position.i:
        self.board[i]['text'] = ''
        self.board[i]['command'] = lambda: None
      else:
        self.board[i]['text'] = repr(self.position[i])
        if i - 1 == self.position.i:
          self.board[i]['command'] = self.right
        elif i + self.n == self.position.i:
          self.board[i]['command'] = self.up
        elif i + 1 == self.position.i:
          self.board[i]['command'] = self.left
        elif i - self.n == self.position.i:
          self.board[i]['command'] = self.down
        else:
          self.board[i]['command'] = lambda: None


def main():
  root = Tk()
  app = Application(master=root)
  app.mainloop()
  root.destroy()


if __name__ == "__main__":
  main()

