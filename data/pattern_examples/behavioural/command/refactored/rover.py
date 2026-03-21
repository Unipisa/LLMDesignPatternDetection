from abc import ABC, abstractmethod

# Implementation of a command pattern simulating the movements of a rover.

# invoker
class MissionControl:
    def __init__(self):
        self.commands = []
    def add_command(self, command):
        self.commands.append(command)
    def execute_mission(self):
        for command in self.commands:
            command.execute()

# receiver
class Rover:
    def __init__(self):
        self.x = 0
        self.y = 0
    def move_forward(self, metres):
        self.y += metres
    def move_left(self, metres):
        self.x -= metres
    def move_right(self, metres):
        self.x += metres
    def move_back(self, metres):
        self.y -= metres


# commands
class MovementCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

class MoveForwardCommand(MovementCommand):
    def __init__(self, metres, rover):
        self.metres = metres
        self.rover = rover

    def execute(self):
        self.rover.move_forward(self.metres)

class MoveLeftCommand(MovementCommand):
    def __init__(self, metres, rover):
        self.rover = rover
        self.metres = metres
    def execute(self):
        self.rover.move_left(self.metres)

class MoveRightCommand(MovementCommand):
    def __init__(self, metres, rover):
        self.rover = rover
        self.metres = metres
    def execute(self):
        self.rover.move_right(self.metres)

class MoveBackCommand(MovementCommand):
    def __init__(self, metres, rover):
        self.rover = rover
        self.metres = metres
    def execute(self):
        self.rover.move_back(self.metres)


# client
class MissionManager:
    def __init__(self):
        self.mission_control = MissionControl()
        self.rover = Rover()
    def start(self):
        print(f"Mission started! Rover's position: ({self.rover.x}, {self.rover.y})\n")
        self.mission_control.add_command(MoveForwardCommand(10, self.rover))
        self.mission_control.add_command(MoveLeftCommand(5, self.rover))
        self.mission_control.add_command(MoveBackCommand(2, self.rover))
        self.mission_control.execute_mission()
        print(f"Rover's final position: ({self.rover.x}, {self.rover.y})")

