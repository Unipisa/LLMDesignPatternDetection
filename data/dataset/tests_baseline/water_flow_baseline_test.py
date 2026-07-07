from data.dataset.baseline.water_flow_baseline import PhisicalValve
import unittest

class TestWaterFlowController(unittest.TestCase):
    def test_dispense(self):
        valve = PhisicalValve()
        result = valve.dispense(10)
        self.assertEqual(result, "Dispensed 10 liters of water")

    def test_get_recorded_usage(self):
        valve = PhisicalValve()
        valve.dispense(10)
        usage = valve.get_recorded_usage()
        self.assertEqual(usage[0][1], 10)

    def test_get_recorded_usage_length(self):
        valve = PhisicalValve()
        valve.dispense(10)
        valve.dispense(20)
        valve.dispense(30)
        valve.dispense(15)
        usage = valve.get_recorded_usage()
        self.assertEqual(len(usage), 4)

    def test_get_total_recorded_usage(self):
        valve = PhisicalValve()
        valve.dispense(10)
        valve.dispense(20)
        valve.dispense(15)
        self.assertEqual(sum([x for _, x in valve.get_recorded_usage()]), sum([10, 20, 15]))