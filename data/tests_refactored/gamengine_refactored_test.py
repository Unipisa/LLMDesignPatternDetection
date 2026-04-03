import unittest
from data.refactored.gamengine_refactored import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.dungeon_builder = DungeonBuilder()
        self.darkwoods_builder = DarkWoodsBuilder()
        self.director = Director(None)

    def test_darkwoods_builder(self):
        self.director.change_builder(self.darkwoods_builder)
        self.director.make()
        self.assertEqual(self.darkwoods_builder.get_product()._parts, ["Dense dark forest" ,
                                                                       "Stone ruins and abandoned cabins",
                                                                    "Group of orcs", "Soft moonlight"])

    def test_dungeon_builder(self):
        self.director.change_builder(self.dungeon_builder)
        self.director.make()
        self.assertEqual(self.dungeon_builder.get_product()._parts, ["Rocky and hilly terrain",
                                                                     "Stone walls and pillars",
                                                                     "Group of goblins",
                                                                     "Flickering torches around the walls"])