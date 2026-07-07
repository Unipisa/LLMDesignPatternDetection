import unittest
from data.dataset.baseline.gamengine_baseline import *

class TestGameEngine(unittest.TestCase):
    def test_dungeon(self):
        e = GameEngine(GameEngineType.DUNGEON)
        e.make()
        self.assertEqual(e._parts, ["Rocky and hilly terrain", "Stone walls and pillars", "Group of goblins",
                                                                     "Flickering torches around the walls"])

    def test_darkwoods(self):
        e = GameEngine(GameEngineType.DARKWOODS)
        e.make()
        self.assertEqual(e._parts, ["Dense dark forest", "Stone ruins and abandoned cabins", "Group of orcs",
                                    "Soft moonlight"])