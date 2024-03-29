# Torbert, 11.11.2004

from random import *
from math import *
from sys import *

# handle command line arguments for board dimensions
if len(argv) > 1:
	n = int(argv[1])
else:
	n = 8
max = n * (n - 1) / 2

def show(board):
	print()
	for r in range(n):
		s = ""
		for c in range(n):
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

def main():
	board = list(range(n))
	for k in range(n):
		board[k] = randint(0, n-1)
	show(board)

if __name__ == "__main__":
	main()
