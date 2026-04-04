from enum import Enum

class CombactType(Enum):
    AIR = 1
    GROUND = 2


class Dragon:
    def __init__(self):
        self.weapon = None

    def fight(self):
        return f"Dragon attacks using {self.weapon.get_description()}"

    def equip(self, weapon):
        self.weapon = weapon


class Goblin:
    def __init__(self):
        self.weapon = None

    def fight(self):
        return f"Goblin attacks using {self.weapon.get_description()}"

    def equip(self, weapon):
        self.weapon = weapon


class Sword:
    def get_description(self):
        return "Sword"


class Cannon:
    def get_description(self):
        return "Cannon"


class Combact:
    def __init__(self, combact_type):
        self.combact_type = combact_type
    def fight(self):
        if self.combact_type == CombactType.AIR:
            dragon = Dragon()
            dragon.equip(Cannon())
            return dragon.fight()
        elif self.combact_type == CombactType.GROUND:
            goblin = Goblin()
            goblin.equip(Sword())
            return goblin.fight()
        return None
