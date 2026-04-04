from data.refactored.battle_refactored_af import *
import unittest

class TestCombactFactory(unittest.TestCase,):
    def setUp(self):
        self.f1 = AirCombatFactory()
        self.f2 = GroundCombatFactory()

    def test_air_combact_factory(self):
        monster = self.f1.create_monster()
        weapon = self.f1.create_weapon()
        monster.equip(weapon)
        self.assertEqual(monster.fight(), "Dragon attacks using Cannon")

    def test_ground_combact_factory(self):
        monster = self.f2.create_monster()
        weapon = self.f2.create_weapon()
        monster.equip(weapon)
        self.assertEqual(monster.fight(), "Goblin attacks using Sword")
