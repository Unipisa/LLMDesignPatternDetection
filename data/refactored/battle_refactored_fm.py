from abc import abstractmethod, ABC

class Fighter(ABC):
    @abstractmethod
    def fight(self):
        pass


class Dragon(Fighter):
    def __init__(self):
        self.weapon = None

    def fight(self):
        return f"Dragon attacks using {self.weapon.get_description()}"

    def equip(self, weapon):
        self.weapon = weapon


class Goblin(Fighter):
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

class FighterCreator(ABC):
    @abstractmethod
    def create_fighter(self):
        pass

class DragonFighterCreator(FighterCreator):
    def create_fighter(self):
        fighter = Dragon()
        fighter.equip(Cannon())
        return fighter

class GoblinFighterCreator(FighterCreator):
    def create_fighter(self):
        fighter = Goblin()
        fighter.equip(Sword())
        return fighter



