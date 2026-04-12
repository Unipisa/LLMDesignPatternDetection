from abc import ABC, abstractmethod


# Base component classes
class Wood(ABC):
    def __init__(self, mana: int):
        self.mana = mana

class Core(ABC):
    def __init__(self, damage: int):
        self.damage = damage

class Gem(ABC):
    def __init__(self, power: float):
        self.power = power


# Concrete Wood classes
class Oak(Wood):
    def __init__(self):
        super().__init__(mana=50)

class Willow(Wood):
    def __init__(self):
        super().__init__(mana=40)

class Elder(Wood):
    def __init__(self):
        super().__init__(mana=70)


# Concrete Core classes
class PhoenixFeather(Core):
    def __init__(self):
        super().__init__(damage=100)


# Concrete Gem classes
class Ruby(Gem):
    def __init__(self):
        super().__init__(power=1)

class Sapphire(Gem):
    def __init__(self):
        super().__init__(power=1.25)

class Emerald(Gem):
    def __init__(self):
        super().__init__(power=1.5)


# Wand product class
class Wand:
    def __init__(self, wood: Wood, core: Core, gem: Gem):
        self.wood = wood
        self.core = core
        self.gem = gem

    @property
    def attack(self):
        return self.wood.mana * (self.core.damage ** self.gem.power)

class WandFactory(ABC):
    @abstractmethod
    def create_wand(self) -> Wand:
        pass


class OakPhoenixRubyFactory(WandFactory):
    def create_wand(self) -> Wand:
        wood = Oak()
        core = PhoenixFeather()
        gem = Ruby()
        return Wand(wood, core, gem)

class WillowPhoenixSapphireFactory(WandFactory):
    def create_wand(self) -> Wand:
        wood = Willow()
        core = PhoenixFeather()
        gem = Sapphire()
        return Wand(wood, core, gem)

class ElderPhoenixEmeraldFactory(WandFactory):
    def create_wand(self) -> Wand:
        wood = Elder()
        core = PhoenixFeather()
        gem = Emerald()
        return Wand(wood, core, gem)