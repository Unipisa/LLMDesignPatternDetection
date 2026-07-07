from data.dataset.refactored.house_refactored_fm import *
import unittest

class TestHouse(unittest.TestCase):
    def setUp(self):
        self.apartment = ApartmentCreator().create_house()
        self.town_house = TownHouseCreator().create_house()
        self.villa = VillaCreator().create_house()
    def test_apartment_alarm(self):
        self.assertIsInstance(self.apartment.alarm, NoneAlarm)

    def test_townhouse_alarm(self):
        self.assertIsInstance(self.town_house.alarm, VideoMonitoredAlarm)

    def test_villa_alarm(self):
        self.assertIsInstance(self.villa.alarm, PrivateSecurityAlarm)

    def test_apartment_furniture(self):
        self.assertIsInstance(self.apartment.furniture, ModernFurniture)

    def test_townhouse_furniture(self):
        self.assertIsInstance(self.town_house.furniture, ClassicFurniture)

    def test_villa_furniture(self):
        self.assertIsInstance(self.villa.furniture, RusticFurniture)

    def test_apartment_garden(self):
        self.assertIsInstance(self.apartment.garden, NoneGarden)

    def test_townhouse_garden(self):
        self.assertIsInstance(self.town_house.garden, NoneGarden)

    def test_villa_garden(self):
        self.assertIsInstance(self.villa.garden, FlowerGarden)

    def test_apartment_description(self):
        self.assertEqual(self.apartment.describe(), (
            "Modern vibes only: clear lines, bold ideas!",
            "No garden, no problem!",
            "No alarm, just peace and quiet."))

    def test_townhouse_description(self):
        self.assertEqual(self.town_house.describe(), (
            "Classic is old-fashioned, but still fresh.",
            "No garden, no problem!",
            "Video-monitoring alarm: smile, you are on camera!"))

    def test_villa_description(self):
        self.assertEqual(self.villa.describe(), (
            "Wood, stone and heart: that's rustic style!",
            "Flowers, flowers everywhere!",
            "Private security in action."))