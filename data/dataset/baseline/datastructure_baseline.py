from enum import Enum
from collections import defaultdict

class DataStructureType(Enum):
    GRAPH = 1
    TREE = 2

class Graph:
    def __init__(self):
        self._structure = defaultdict(list)
    def get_structure(self):
        return self._structure
    def __str__(self):
        s=""
        for node, neighbors in self._structure.items():
            s += f"{node} -> {neighbors}\n"
        return s

class Tree:
    def __init__(self):
        self._structure = defaultdict(list)
        self._root = None
    def get_structure(self):
        return self._structure
    def get_root(self):
        return self._root
    def __str__(self):
        def recurse(node, depth=0):
            s = "   " * depth + str(node) + "\n"
            for child in self._structure[node]:
                s += recurse(child, depth + 1)
            return s
        if self._root is None:
            return "empty tree"
        return recurse(self._root)


class Structure:
    def __init__(self, t: DataStructureType):
        self._type = t
        self._structure = defaultdict(list)
        if t == DataStructureType.TREE:
            self._root = None

    def get_root(self):
        return self._root

    def add_node(self, node):
        if self._type == DataStructureType.TREE:
            if not self._structure:  # empty tree
                self._root = node
            _ = self._structure[node]
        elif self._type == DataStructureType.GRAPH:
            _ = self._structure[node]

    def add_edge(self, node1, node2):
        if self._type == DataStructureType.GRAPH and node2 not in self._structure[node1]:
                self._structure[node1].append(node2)
        elif (self._type == DataStructureType.TREE and node2 not in [x for i in self._structure.values() for x in i] and
              not (node1 == node2) and node2 != self.get_root()):
                self._structure[node1].append(node2)

    def get_structure(self):
        return self._structure

    def make(self):
        for node in range(5):  # nodi 0..4
            self.add_node(node)
        self.add_edge(0, 1)
        self.add_edge(0, 2)
        self.add_edge(1, 2)
        self.add_edge(2, 3)
        self.add_edge(3, 4)
        self.add_edge(1, 4)

