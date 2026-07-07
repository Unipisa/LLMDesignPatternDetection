from data.dataset.baseline.battle_baseline import *
import unittest

class TestBattle(unittest.TestCase,):
    def test_air_combact(self):
        combact = Combact(CombactType.AIR)
        self.assertEqual(combact.fight(), "Dragon attacks using Cannon")

    def test_ground_combact(self):
        combact = Combact(CombactType.GROUND)
        self.assertEqual(combact.fight(), "Goblin attacks using Sword")