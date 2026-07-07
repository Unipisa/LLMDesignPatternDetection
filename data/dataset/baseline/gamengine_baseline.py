from enum import Enum

class GameEngineType(Enum):
    DUNGEON = 1
    DARKWOODS = 2

class GameEngine:
    def __init__(self, t: GameEngineType):
        self.type = t

        # default values need to be changed
        self._parts = ["terrain_shape", "structures", "interactive_entities", "light"]

    def make(self):
        if self.type == GameEngineType.DUNGEON:
            self._parts[0] = "Rocky and hilly terrain"
            self._parts[1] = "Stone walls and pillars"
            self._parts[2] = "Group of goblins"
            self._parts[3] = "Flickering torches around the walls"
        elif self.type == GameEngineType.DARKWOODS:
            self._parts[0] = "Dense dark forest"
            self._parts[1] = "Stone ruins and abandoned cabins"
            self._parts[2] = "Group of orcs"
            self._parts[3] = "Soft moonlight"