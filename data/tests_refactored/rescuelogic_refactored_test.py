from data.refactored.rescuelogic_refactored import MountainRescue, MaritimeRescue
import unittest

class TestRescueLogic(unittest.TestCase):
    def test_mountain_rescue_ground(self):
        mission = MountainRescue(True, 100, 200, 3000)
        mission.start_rescue()
        self.assertEqual(mission.log, ["Dispatch alpine rescue team", "Mission completed"])
    def test_mountain_rescue_ground2(self):
        mission = MountainRescue(False, 100, 200, 3000)
        mission.start_rescue()
        self.assertEqual(mission.log, ["Altitude too low for helicopter", "Dispatch alpine rescue team", "Mission completed"])
    def test_mountain_rescue_helicopter(self):
        mission = MountainRescue(False, 100, 200, 4000)
        mission.start_rescue()
        self.assertEqual(mission.log, ["Taking off", "Mission completed"])
    def test_maritime_rescue_helicopter(self):
        mission = MaritimeRescue(False, 100, 200, 1000)
        mission.start_rescue()
        self.assertEqual(mission.log, ["Taking off", "Mission completed"])
    def test_maritime_rescue_ground(self):
        mission = MaritimeRescue(True, 100, 200, 1000)
        mission.start_rescue()
        self.assertEqual(mission.log, ["Sent maritime rescue team", "Mission completed"])

if __name__ == "__main__":
    unittest.main()