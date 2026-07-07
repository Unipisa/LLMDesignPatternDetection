from data.dataset.refactored.battle_refactored_fm import *
import unittest

class TestFighterCreator(unittest.TestCase):
    def setUp(self):
        self.dragon = DragonFighterCreator().create_fighter()
        self.goblin = GoblinFighterCreator().create_fighter()

    def test_dragon_fighter(self):
        self.assertIsInstance(self.dragon, Dragon)

    def test_goblin_fighter(self):
        self.assertIsInstance(self.goblin, Goblin)

    def test_dragon_weapon(self):
        self.assertIsInstance(self.dragon.weapon, Cannon)

    def test_goblin_weapon(self):
        self.assertIsInstance(self.goblin.weapon, Sword)

    def test_dragon_fighter_fight(self):
        self.assertEqual(self.dragon.fight(), "Dragon attacks using Cannon")

    def test_goblin_fighter_fight(self):
        self.assertEqual(self.goblin.fight(), "Goblin attacks using Sword")