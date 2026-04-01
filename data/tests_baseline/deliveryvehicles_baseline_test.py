from data.baseline.deliveryvehicles_baseline import *
import unittest

class TestDelyberySystem(unittest.TestCase):
    def setUp(self):
        self.driver = DeliverySystem(124)
        self.admin = DeliverySystem(7)
        self.unknown = DeliverySystem(1000)
    def test_proxy_driver_get_delivery_route(self):
        self.assertEqual(self.driver.get_delivery_route("AB123CD"),
                         "Nomentana Street → East Ring Road → Tiburtina Street")
    def test_proxy_driver_get_traffic_status(self):
        self.assertEqual(self.driver.get_traffic_status("IJ789KL"), "light traffic")
    def test_proxy_driver_get_veichle_status(self):
        self.assertEqual(self.driver.get_vehicle_status("MN012OP"), 40)
    def test_proxy_driver_set_driver(self):
        self.assertEqual(self.driver.set_driver(101, "IJ789KL"), "Access denied")
        self.assertEqual(self.driver.get_vehicle_status("IJ789KL"), 305)
    def test_proxy_driver_set_delivery_route(self):
        self.assertEqual(self.driver.set_delivery_route("EF456GH", "Oak Lane → Industrial Park"),
                         "Access denied")
        self.assertEqual(self.driver.get_delivery_route("EF456GH"),
                         "Appia Street → Ring Road → Tuscolana Street")
    def test_proxy_admin_get_delivery_route(self):
        self.assertEqual(self.admin.get_delivery_route("AB123CD"),
                         "Nomentana Street → East Ring Road → Tiburtina Street")
    def test_proxy_admin_get_traffic_status(self):
        self.assertEqual(self.admin.get_traffic_status("IJ789KL"), "light traffic")
    def test_proxy_admin_get_vehicle_status(self):
        self.assertEqual(self.admin.get_vehicle_status("MN012OP"), 40)
    def test_proxy_admin_set_driver(self):
        self.assertEqual(self.admin.set_driver(101, "IJ789KL"), "Done")
        self.assertEqual(self.admin.get_vehicle_status("IJ789KL"), 101)
    def test_proxy_admin_set_delivery_route(self):
        self.assertEqual(self.admin.set_delivery_route("EF456GH", "Oak Lane → Industrial Park"),
                         "Done")
        self.assertEqual(self.admin.get_delivery_route("EF456GH"), "Oak Lane → Industrial Park")
    def test_proxy_unknown_get_delivery_route(self):
        self.assertEqual(self.unknown.get_delivery_route("AB123CD"), "Access denied")
    def test_proxy_unknown_get_vehicle_status(self):
        self.assertEqual(self.unknown.get_vehicle_status("MN012OP"), "Access denied")
    def test_proxy_unknown_get_traffic_status(self):
        self.assertEqual(self.unknown.get_traffic_status("IJ789KL"), "Access denied")
    def test_proxy_unknown_set_driver(self):
        self.assertEqual(self.unknown.set_driver(101, "IJ789KL"), "Access denied")
    def test_proxy_unknown_set_delivery_route(self):
        self.assertEqual(self.unknown.set_delivery_route("EF456GH", "Oak Lane → Industrial Park"),
                         "Access denied")