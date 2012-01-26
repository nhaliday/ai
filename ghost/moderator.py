#!/usr/bin/env python3
# Nick Haliday
# Torbert, period 1
# GHOST Moderator

import cmd
import sys
import shlex
import trie


class Moderator:

    INVALID = 1
    GHOST = 5

    def __init__(self, dictionary, charchoice, numplayers=2):
        self.root = trie.build(dictionary)
        self.string = ""
        self.state = self.root
        self.player = 0
        self.ghost = [0] * numplayers
        self.charchoice = charchoice
        self.numplayers = numplayers

    def move(self, char):
        oldplayer = self.player
        char = char

        while True:
            self.string += char
            if self.state != Moderator.INVALID:
                try:
                    self.state = self.state.children[char]
                except KeyError:
                    self.state = Moderator.INVALID

            self.player = self.next()
            if self.player == oldplayer:
                break
            char = charchoice[self.player](self.string, self.state)

    def lose(self, player=None):
        if player is None:
            player = self.player
        self.ghost[player] += 1
        if self.ghost[player] >= Moderator.GHOST:
            print("{0}: GHOST")

    def challenge(self):
        if self.state == Moderator.INVALID or self.state.end:
            self.lose(self.last())
        else:
            self.lose()
        self.string = ""
        self.state = self.root
        self.player = self.next()

    def next(self, player=None):
        if player is None:
            player = self.player
        return (player + 1) % self.numplayers

    def last(self, player=None):
        if player is None:
            player = self.player
        return (player - 1) % self.numplayers


def split(f):
    def g(self, line):
        args = shlex.split(line)
        return f(self, *args)
    return g


class Repl(cmd.Cmd):

    def __init__(self, dictionary, charchoice, numplayers=2, completekey='tab', stdin=None, stdout=None):
        self.moderator = Moderator(dictionary, charchoice, numplayers)
        self.prompt = '(Ghost) '
        super().__init__(completekey, stdin, stdout)

    @split
    def do_move(self, char):
        """Move interface for humans"""
        self.moderator.move(char)

    @split
    def do_state(self):
        """Print out the current game state"""
        print(self.moderator.state)

    @split
    def do_challenge(self):
        """Challenge the current string"""
        self.moderator.challenge()

    @split
    def do_EOF(self):
        """Quit the program"""
        sys.exit()


def main():
    with open('dictionary.txt') as fin:
        text = fin.read().split()[:-1]
    repl = Repl(text)
    repl.cmdloop()


if __name__ == "__main__":
    main()
