from abc import ABC, abstractmethod
from collections import defaultdict


# builder for graph and tree data structures
# using adjacency list representation

# abstract builder interface
class DataStructureBuilder(ABC):
    def __init__(self):
        self._product = None
        self.reset()

    def reset(self):
        pass

    @abstractmethod
    def add_node(self, node):
        pass

    @abstractmethod
    def add_edge(self, node1, node2):
        pass

    def get_product(self):
        product = self._product
        self.reset()
        return product

# concrete products
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

# concrete builders
class GraphBuilder(DataStructureBuilder):
    def reset(self):
        self._product = Graph()
    def add_node(self, node):
        _ = self._product.get_structure()[node]
    def add_edge(self, node1, node2):
        if node2 not in self._product.get_structure()[node1]:
            self._product.get_structure()[node1].append(node2)


class TreeBuilder(DataStructureBuilder):
    def reset(self):
        self._product = Tree()
    def add_node(self, node):
        if not self._product.get_structure():  # empty tree
            self._product._root = node
        _ = self._product.get_structure()[node]
    def add_edge(self, node1, node2):
        if (node2 not in [x for i in self._product.get_structure().values() for x in i] and not (node1 == node2) and
                node2 != self._product.get_root()):
            self._product.get_structure()[node1].append(node2)


class Director:
    def __init__(self, builder):
        self._builder = builder
    def change_builder(self, builder):
        self._builder = builder
    def make(self):
        self._builder.reset()
        for node in range(5):  # nodi 0..4
            self._builder.add_node(node)
            # aggiungo archi arbitrari
        self._builder.add_edge(0, 1)
        self._builder.add_edge(0, 2)
        self._builder.add_edge(1, 2)
        self._builder.add_edge(2, 3)
        self._builder.add_edge(3, 4)
        self._builder.add_edge(1, 4)
