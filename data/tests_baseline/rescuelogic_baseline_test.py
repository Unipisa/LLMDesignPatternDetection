from data.baseline.rescuelogic_baseline import *
import unittest

class TestRescueLogic(unittest.TestCase):
    def test_mountain_rescue_ground(self):
        rescue = RescueMission(RescueType.MOUNTAIN, True, 100, 200, 3000)
        rescue.start_rescue()
        self.assertEqual(rescue.log, ["Dispatch alpine rescue team", "Mission completed"])
    def test_mountain_rescue_ground2(self):
        rescue = RescueMission(RescueType.MOUNTAIN, False, 100, 200, 3000)
        rescue.start_rescue()
        self.assertEqual(rescue.log, ["Altitude too low for helicopter", "Dispatch alpine rescue team", "Mission completed"])
    def test_mountain_rescue_helicopter(self):
        rescue = RescueMission(RescueType.MOUNTAIN, False, 100, 200, 4000)
        rescue.start_rescue()
        self.assertEqual(rescue.log, ["Taking off", "Mission completed"])
    def test_maritime_rescue_helicopter(self):
        rescue = RescueMission(RescueType.MARITIME, False, 100, 200, 1000)
        rescue.start_rescue()
        self.assertEqual(rescue.log, ["Taking off", "Mission completed"])
    def test_maritime_rescue_ground(self):
        rescue = RescueMission(RescueType.MARITIME, True, 100, 200, 1000)
        rescue.start_rescue()
        self.assertEqual(rescue.log, ["Sent maritime rescue team", "Mission completed"])