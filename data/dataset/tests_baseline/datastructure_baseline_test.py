from data.dataset.baseline.datastructure_baseline import *
import unittest

class TestStructure(unittest.TestCase,):
    def setUp(self):
        self.tree = Structure(DataStructureType.TREE)
        self.graph = Structure(DataStructureType.GRAPH)

    def test(self):
        self.graph.make()
        self.assertEqual(self.graph.get_structure(), {
                                                                0: [1, 2],
                                                                1: [2, 4],
                                                                2: [3],
                                                                3: [4],
                                                                4: []
                                                            })

    def test_tree(self):
        self.tree.make()
        self.assertEqual(self.tree.get_structure(),{
                                                            0: [1, 2],
                                                            1: [],
                                                            2: [3],
                                                            3: [4],
                                                            4: []
                                                            })