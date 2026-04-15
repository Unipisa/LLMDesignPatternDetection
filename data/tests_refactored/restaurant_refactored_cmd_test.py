import unittest
from data.refactored.restaurant_refactored_cmd import (Waiter, GrillCommand, FryCommand, PourCommand, TableMacroOrder,
                                                       Kitchen)

class TestKitchen(unittest.TestCase):
    def setUp(self):
        self.kitchen = Kitchen()
    def test_pour(self):
        self.assertEqual(self.kitchen.pour("tea"), "Served tea")
    def test_grill(self):
        self.assertEqual(self.kitchen.grill("steak"), "Grilled steak")
    def test_fry(self):
        self.assertEqual(self.kitchen.fry("rice"), "Fried rice")



class TestWaiter(unittest.TestCase):
    def test_serve_orders(self):
        kitchen = Kitchen()
        waiter = Waiter(TableMacroOrder(1, GrillCommand("steak", kitchen), FryCommand("rice", kitchen)))
        self.assertEqual(waiter.serve(), "Table 1 ready with: Grilled steak, Fried rice")
    def test_serve_order(self):
        kitchen = Kitchen()
        waiter = Waiter(GrillCommand("steak", kitchen))
        self.assertEqual(waiter.serve(), "Grilled steak")

class TestOrderCommands(unittest.TestCase):
    def setUp(self):
        self.kitchen = Kitchen()
    def test_grill_command(self):
        command = GrillCommand("steak", self.kitchen)
        self.assertEqual(command.execute(), "Grilled steak")
    def test_fry_command(self):
        command = FryCommand("rice", self.kitchen)
        self.assertEqual(command.execute(), "Fried rice")
    def test_pour_command(self):
        command = PourCommand("tea", self.kitchen)
        self.assertEqual(command.execute(), "Served tea")
    def test_table_macro_order(self):
        order = TableMacroOrder(1, GrillCommand("steak", self.kitchen), FryCommand("rice", self.kitchen))
        self.assertEqual(order.execute(), "Table 1 ready with: Grilled steak, Fried rice")