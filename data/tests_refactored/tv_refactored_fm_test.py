from data.refactored.tv_refactored_fm import *
import unittest

class TestCreateBox(unittest.TestCase):
    def setUp(self):
        self.samsung_box = CreateSamsungBox().create_box()
        self.philips_box = CreatePhilipsBox().create_box()

    def test_samsung_box_tv(self):
        self.assertIsInstance(self.samsung_box.tv, SamsungTV)

    def test_philips_box_tv(self):
        self.assertIsInstance(self.philips_box.tv, PhilipsTV)

    def test_samsung_box_rc(self):
        self.assertIsInstance(self.samsung_box.rc, SamsungRC)

    def test_philips_box_rc(self):
        self.assertIsInstance(self.philips_box.rc, PhilipsRC)

    def test_samsung_box_description(self):
        self.assertEqual(self.samsung_box.get_description(), "Box with Samsung TV and Samsung RC")

    def test_philips_box_description(self):
        self.assertEqual(self.philips_box.get_description(), "Box with Philips TV and Philips RC")