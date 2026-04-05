import unittest

from data.refactored.house_refactored_af import *

class TestHouse(unittest.TestCase):
    def setUp(self):
        self.apartment = Apartment()
        self.TownHouse = TownHouse()
        self.Villa = Villa()

    def test_apartment_furniture(self):
        self.assertEqual(self.apartment.create_furniture().get_style(), "Modern vibes only: clear lines, bold "
                                                                        "ideas!")

    def test_townhouse_furniture(self):
        self.assertEqual(self.TownHouse.create_furniture().get_style(), "Classic is old-fashioned, but still "
                                                                        "fresh.")

    def test_villa_furniture(self):
        self.assertEqual(self.Villa.create_furniture().get_style(), "Wood, stone and heart: that's rustic "
                                                                    "style!")

    def test_apartment_garden(self):
        self.assertEqual(self.apartment.create_garden().get_description(), "No garden, no problem!")

    def test_townhouse_garden(self):
        self.assertEqual(self.TownHouse.create_garden().get_description(), "No garden, no problem!")

    def test_villa_garden(self):
        self.assertEqual(self.Villa.create_garden().get_description(), "Flowers, flowers everywhere!")

    def test_apartment_alarm(self):
        self.assertEqual(self.apartment.create_alarm().get_defense(), "No alarm, just peace and quiet.")

    def test_townhouse_alarm(self):
        self.assertEqual(self.TownHouse.create_alarm().get_defense(), "Video-monitoring alarm: smile, you are "
                                                                      "on camera!")

    def test_villa_alarm(self):
        self.assertEqual(self.Villa.create_alarm().get_defense(), "Private security in action.")



