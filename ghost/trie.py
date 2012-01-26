#!/usr/bin/env python3
# Nick Haliday, 5 November 2011
# Torbert, period 1
# Trie

class Trie:

    def __init__(self, char='^', children=None, end=False, parent=None):
        self.char = char
        self.children = children if children is not None else {}
        self.end = end
        self.attach(parent)

    def _strhelper(self, indent=0):
        tab = '  ' * indent
        return (tab + self.char + ('*' if self.end else ' ') + '\n' +
                '\n'.join(self.children[k]._strhelper(indent + 1) for k
                in sorted(self.children)))

    def __str__(self):
        return self._strhelper()

    def __repr__(self):
        return """{0}(char={char}, children={children!r},
            end={end})""".format(self.__class__.__name__,
            char=self.char, children=self.children, end=self.end,
            parent=self.parent)

    def attach(self, parent):
        self.parent = parent
        self.depth = 0 if parent is None else parent.depth + 1
        for node in self.children.values():
            node.attach(self)

    def transition(char):
        return node.children[char]

    def lookup(self, s):
        node = self
        for ch in s:
            if ch not in node.children:
                break
            else:
                node = node.children[ch]
        return node

    def insert(self, s):
        node = self.lookup(s)
        for ch in s[node.depth - self.depth:]:
            node.children[ch] = Trie(ch, parent=node)
            node = node.children[ch]
        node.end = True
        return node

    def match(self, s):
        node = self.lookup(s)
        return node.depth - self.depth == len(s) and node.end


def build(dictionary):
    root = Trie()
    for word in dictionary:
        root.insert(word)
    return root


def main():
    root = Trie()
    with open('dictionary.txt') as fin:
        for line in fin:
            root.insert(line.strip())
    with open('wordtree.txt', 'w') as fout:
        print(root, file=fout)


if __name__ == "__main__":
    main()
