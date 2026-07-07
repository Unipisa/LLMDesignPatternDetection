from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List # simplifies uml diagram generation

# Implementation of a command pattern simulating the movements of a rover.

# invoker
class MissionControl:
    def __init__(self):
        self.commands: List[MovementCommand] = []
    def add_command(self, command: MovementCommand)-> None:
        self.commands.append(command)
    def execute_mission(self)-> None:
        for command in self.commands:
            command.execute()

# receiver
class Rover:
    def __init__(self):
        self.x = 0
        self.y = 0
    def move_forward(self, metres: int) -> None:
        self.y += metres
    def move_left(self, metres: int) -> None:
        self.x -= metres
    def move_right(self, metres: int) -> None:
        self.x += metres
    def move_back(self, metres: int) -> None:
        self.y -= metres


# commands
class MovementCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class MoveForwardCommand(MovementCommand):
    def __init__(self, metres: int, rover: Rover)-> None:
        self.metres = metres
        self.rover = rover

    def execute(self) -> None:
        self.rover.move_forward(self.metres)

class MoveLeftCommand(MovementCommand):
    def __init__(self, metres: int, rover: Rover)-> None:
        self.rover = rover
        self.metres = metres
    def execute(self)-> None:
        self.rover.move_left(self.metres)

class MoveRightCommand(MovementCommand):
    def __init__(self, metres: int, rover: Rover)-> None:
        self.rover = rover
        self.metres = metres
    def execute(self)-> None:
        self.rover.move_right(self.metres)

class MoveBackCommand(MovementCommand):
    def __init__(self, metres: int, rover: Rover) -> None:
        self.rover = rover
        self.metres = metres
    def execute(self)-> None:
        self.rover.move_back(self.metres)

