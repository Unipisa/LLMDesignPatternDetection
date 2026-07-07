import unittest
from data.dataset.refactored.rover_refactored_cmd import MissionControl, Rover, MoveForwardCommand, MoveLeftCommand, MoveRightCommand, MoveBackCommand

class TestRover(unittest.TestCase):
    def setUp(self):
        self.rover = Rover()
    def test_move_forward(self):
        self.rover.move_forward(50)
        self.assertEqual(self.rover.y, 50)
    def test_move_left(self):
        self.rover.move_left(50)
        self.assertEqual(self.rover.x, -50)
    def test_move_right(self):
        self.rover.move_right(50)
        self.assertEqual(self.rover.x, 50)
    def test_move_back(self):
        self.rover.move_back(50)
        self.assertEqual(self.rover.y, -50)

class TestMissionControl(unittest.TestCase):
    def setUp(self):
        self.mission_control = MissionControl()
        self.rover = Rover()
    def test_add_command(self):
        self.mission_control.add_command(MoveForwardCommand(15, self.rover))
        self.mission_control.add_command(MoveLeftCommand(100, self.rover))
        self.assertEqual(len(self.mission_control.commands), 2)
    def test_execute_mission(self):
        self.mission_control.add_command(MoveForwardCommand(15, self.rover))
        self.mission_control.add_command(MoveLeftCommand(100, self.rover))
        self.mission_control.execute_mission()
        self.assertEqual(self.rover.x, -100)
        self.assertEqual(self.rover.y, 15)

class TestMovementCommands(unittest.TestCase):
    def setUp(self):
        self.rover = Rover()
    def test_move_forward(self):
        command = MoveForwardCommand(10, self.rover)
        command.execute()
        self.assertEqual(self.rover.y, 10)
    def test_move_left(self):
        command = MoveLeftCommand(10, self.rover)
        command.execute()
        self.assertEqual(self.rover.x, -10)
    def test_move_right(self):
        command = MoveRightCommand(10, self.rover)
        command.execute()
        self.assertEqual(self.rover.x, 10)
    def test_move_back(self):
        command = MoveBackCommand(5, self.rover)
        command.execute()
        self.assertEqual(self.rover.y, -5)

if __name__ == "__main__":
    unittest.main()