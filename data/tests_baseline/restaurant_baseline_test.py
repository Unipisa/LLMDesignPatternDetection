import unittest
from data.baseline.restaurant_baseline import Waiter, Kitchen

class TestKitchen(unittest.TestCase):
    def setUp(self):
        self.kitchen = Kitchen()
    def test_pour(self):
        self.assertEqual(self.kitchen.pour("tea"), "Served tea")
    def test_grill(self):
        self.assertEqual(self.kitchen.grill("steak"), "Grilled steak")
    def test_fry(self):
        self.assertEqual(self.kitchen.fry("chicken"), "Fried chicken")

class TestWaiter(unittest.TestCase):
    def test_table(self):
        kitchen = Kitchen()
        waiter = Waiter(kitchen)
        self.assertEqual(waiter.serve_table(1, ("grill", "steak"), ("fry", "chicken")), "Table 1 ready with: Grilled steak, Fried chicken")
    def test_drink(self):
        kitchen = Kitchen()
        waiter = Waiter(kitchen)
        self.assertEqual(waiter.serve_drink("tea"), "Served tea")
    def test_grill(self):
        kitchen = Kitchen()
        waiter = Waiter(kitchen)
        self.assertEqual(waiter.serve_grilled("steak"), "Grilled steak")
    def test_fry(self):
        kitchen = Kitchen()
        waiter = Waiter(kitchen)
        self.assertEqual(waiter.serve_fried("chicken"), "Fried chicken")