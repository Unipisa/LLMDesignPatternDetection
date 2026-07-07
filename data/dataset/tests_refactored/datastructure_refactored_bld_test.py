from data.dataset.refactored.datastructure_refactored_bld import *
import unittest

class TestDataStructure(unittest.TestCase):
    def setUp(self):
        self.director = Director(None)
        self.tree_builder = TreeBuilder()
        self.graph_builder = GraphBuilder()

    def test_graph(self):
        self.director.change_builder(self.graph_builder)
        self.director.make()
        self.assertEqual(dict(self.graph_builder.get_product()._structure), {
                                                                    0: [1, 2],
                                                                    1: [2, 4],
                                                                    2: [3],
                                                                    3: [4],
                                                                    4: []
                                                                    })

    def test_tree(self):
        self.director.change_builder(self.tree_builder)
        self.director.make()
        self.assertEqual(dict(self.tree_builder.get_product()._structure), {
                                                                                    0: [1, 2],
                                                                                    1: [],
                                                                                    2: [3],
                                                                                    3: [4],
                                                                                    4: []
                                                                                    })