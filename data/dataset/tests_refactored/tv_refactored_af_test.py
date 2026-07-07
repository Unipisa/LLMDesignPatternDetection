from data.dataset.refactored.tv_refactored_af import *
import unittest

class TestBox(unittest.TestCase):
    def setUp(self):
        self.samsung_factory = SamsungBox()
        self.philips_factory = PhilipsBox()

    def test_samsung_tv(self):
        self.assertEqual(self.samsung_factory.create_tv().get_description(), "Samsung TV")

    def test_samsung_rc(self):
        self.assertEqual(self.samsung_factory.create_rc().get_description(), "Samsung RC")

    def test_philips_tv(self):
        self.assertEqual(self.philips_factory.create_tv().get_description(), "Philips TV")

    def test_philips_rc(self):
        self.assertEqual(self.philips_factory.create_rc().get_description(), "Philips RC")