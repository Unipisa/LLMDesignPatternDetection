import unittest
from data.baseline.rover_baseline import Rover

class TestRover(unittest.TestCase):
    def setUp(self):
        self.rover = Rover()
    def test_move_forward(self):
        self.rover.move_forward(50)
        self.assertEqual(self.rover.y, 50)
    def test_move_left(self):
        self.rover.move_left(150)
        self.assertEqual(self.rover.x, -150)
    def test_move_right(self):
        self.rover.move_right(100)
        self.assertEqual(self.rover.x, 100)
    def test_move_back(self):
        self.rover.move_back(1)
        self.assertEqual(self.rover.y, -1)