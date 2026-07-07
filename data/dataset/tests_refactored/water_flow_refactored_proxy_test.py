from data.dataset.refactored.water_flow_refactored_proxy import (PhisicalValve, WaterFlowController)
import unittest

class TestWaterFlowController(unittest.TestCase):
    def test_dispense(self):
        valve = PhisicalValve()
        controller = WaterFlowController(valve)
        result = controller.dispense(10)
        self.assertEqual(result, "Dispensed 10 liters of water")

    def test_dispense_with_no_valve(self):
        controller = WaterFlowController(None)
        result = controller.dispense(10)
        self.assertEqual(result, "No valve available")

    def test_get_recorded_usage(self):
        valve = PhisicalValve()
        controller = WaterFlowController(valve)
        controller.dispense(10)
        usage = controller.get_recorded_usage()
        self.assertEqual(usage[0][1], 10)

    def test_get_recorded_usage_length(self):
        valve = PhisicalValve()
        controller = WaterFlowController(valve)
        controller.dispense(10)
        controller.dispense(20)
        controller.dispense(30)
        controller.dispense(15)
        usage = controller.get_recorded_usage()
        self.assertEqual(len(usage), 4)

    def test_get_total_recorded_usage(self):
        valve = PhisicalValve()
        controller = WaterFlowController(valve)
        controller.dispense(10)
        controller.dispense(20)
        controller.dispense(15)
        self.assertEqual(sum([x for _, x in controller.get_recorded_usage()]), sum([10, 20, 15]))