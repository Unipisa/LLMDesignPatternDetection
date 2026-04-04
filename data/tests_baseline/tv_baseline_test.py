from data.baseline.tv_baseline import *
import unittest

from data.refactored.tv_refactored_af import SamsungBox, PhilipsBox


class TestBox(unittest.TestCase):
    def setUp(self):
        self.samsung_box = SamsungBox()
        self.philips_box = PhilipsBox()

    def test_samsung_tv(self):
        self.assertEqual(self.samsung_box.create_tv().get_description(), "Samsung TV")

    def test_philips_tv(self):
        self.assertEqual(self.philips_box.create_tv().get_description(), "Philips TV")

    def test_samsung_rc(self):
        self.assertEqual(self.samsung_box.create_rc().get_description(), "Samsung RC")

    def test_philips_rc(self):
        self.assertEqual(self.philips_box.create_rc().get_description(), "Philips RC")