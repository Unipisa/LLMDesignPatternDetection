from data.dataset.baseline.house_baseline import *
import unittest



class TestHouse(unittest.TestCase):
    def setUp(self):
        self.apartment = House(HouseType.APARTMENT)
        self.TownHouse = House(HouseType.TOWNHOUSE)
        self.Villa = House(HouseType.VILLA)

    def test_apartment_furniture(self):
        self.assertEqual(self.apartment.describe()[0], "Modern vibes only: clear lines, bold ideas!")

    def test_townhouse_furniture(self):
        self.assertEqual(self.TownHouse.describe()[0], "Classic is old-fashioned, but still fresh.")

    def test_villa_furniture(self):
        self.assertEqual(self.Villa.describe()[0], "Wood, stone and heart: that's rustic style!")

    def test_apartment_garden(self):
        self.assertEqual(self.apartment.describe()[1], "No garden, no problem!")

    def test_townhouse_garden(self):
        self.assertEqual(self.TownHouse.describe()[1], "No garden, no problem!")

    def test_villa_garden(self):
        self.assertEqual(self.Villa.describe()[1], "Flowers, flowers everywhere!")

    def test_apartment_alarm(self):
        self.assertEqual(self.apartment.describe()[2], "No alarm, just peace and quiet.")

    def test_townhouse_alarm(self):
        self.assertEqual(self.TownHouse.describe()[2], "Video-monitoring alarm: smile, you are on camera!")

    def test_villa_alarm(self):
        self.assertEqual(self.Villa.describe()[2], "Private security in action.")