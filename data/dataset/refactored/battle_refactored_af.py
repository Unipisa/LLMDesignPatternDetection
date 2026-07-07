from abc import ABC, abstractmethod

# CONCRETE PRODUCTS:
# There are 2 types of monsters: Dragon, Goblin
# There are 2 types of weapons: Sword, Cannon

# FAMILIES:
# AirCombactFactory: creates flying monsters equipped with distance weapons
# GroundCombactFactory: creates ground monsters equipped with melee weapons

# abstract products
class Weapon(ABC):
    @abstractmethod
    def get_description(self):
        pass

class Monster (ABC):
    def __init__(self):
        self.weapon = None
    def equip(self, weapon: Weapon):
        self.weapon = weapon
    @ abstractmethod
    def fight(self):
        pass

# concrete products
class Dragon (Monster):
    def fight(self):
        return f"Dragon attacks using {self.weapon.get_description()}"

class Goblin(Monster):
    def fight(self):
        return f"Goblin attacks using {self.weapon.get_description()}"

class Sword(Weapon):
    def get_description(self):
        return "Sword"

class Cannon(Weapon):
    def get_description(self):
        return "Cannon"

# abstract factory
class CombactFactory(ABC):
    @abstractmethod
    def create_monster(self):
        pass
    @abstractmethod
    def create_weapon(self):
        pass


# concrete factories
class AirCombatFactory(CombactFactory):
    def create_monster(self):
        return Dragon()
    def create_weapon(self):
        return Cannon()

class GroundCombatFactory(CombactFactory):
    def create_monster(self):
        return Goblin()
    def create_weapon(self):
        return Sword()
