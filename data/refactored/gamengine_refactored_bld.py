from abc import ABC, abstractmethod

# example of a builder for environments in a game engine.

# interface
class EnvironmentBuilder(ABC):
    @abstractmethod
    def reset(self):
        pass
    @abstractmethod
    def build_terrain_shape(self):
        pass
    @abstractmethod
    def build_structures(self):
        pass
    @abstractmethod
    def build_interactive_entities(self):
        pass
    @abstractmethod
    def build_light(self):
        pass

# products
class Dungeon:
    def __init__(self):
        self._parts = []
    def add_part(self, part):
        self._parts.append(part)
    def __str__(self):
        return "\n".join(self._parts)

class DarkWoods:
    def __init__(self):
        self._parts = []
    def add_part(self, part):
        self._parts.append(part)
    def __str__(self):
        return "\n".join(self._parts)

# concrete builders
class DungeonBuilder(EnvironmentBuilder):
    def __init__(self):
        self._product = None
        self.reset()
    def reset(self):
        self._product = Dungeon()
    def build_terrain_shape(self):
        self._product.add_part("Rocky and hilly terrain")
    def build_structures(self):
        self._product.add_part("Stone walls and pillars")
    def build_interactive_entities(self):
        self._product.add_part("Group of goblins")
    def build_light(self):
        self._product.add_part("Flickering torches around the walls")
    def get_product(self):
        product = self._product
        self.reset()
        return product

class DarkWoodsBuilder(EnvironmentBuilder):
    def __init__(self):
        self._product = None
        self.reset()
    def reset(self):
        self._product = DarkWoods()
    def build_terrain_shape(self):
        self._product.add_part("Dense dark forest")
    def build_structures(self):
        self._product.add_part("Stone ruins and abandoned cabins")
    def build_interactive_entities(self):
        self._product.add_part("Group of orcs")
    def build_light(self):
        self._product.add_part("Soft moonlight")
    def get_product(self):
        product = self._product
        self.reset()
        return product

# director
class Director:
    def __init__(self, builder: EnvironmentBuilder):
        self._builder = builder
    def change_builder(self, builder):
        self._builder = builder
    def make(self):
        self._builder.reset()
        self._builder.build_terrain_shape()
        self._builder.build_structures()
        self._builder.build_interactive_entities()
        self._builder.build_light()
