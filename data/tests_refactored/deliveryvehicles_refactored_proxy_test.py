from data.refactored.deliveryvehicles_refactored_proxy import *
import unittest

class TestDeliveryProxy(unittest.TestCase):
    def setUp(self):
        self.proxy_driver = DeliveryProxy(DeliveryDB(), 124)
        self.proxy_admin = DeliveryProxy(DeliveryDB(), 7)
        self.proxy_unknown = DeliveryProxy(DeliveryDB(), 1000)
    def test_proxy_driver_get_delivery_route(self):
        self.assertEqual(self.proxy_driver.get_delivery_route("AB123CD"),
                         "Nomentana Street → East Ring Road → Tiburtina Street")
    def test_proxy_driver_get_traffic_status(self):
        self.assertEqual(self.proxy_driver.get_traffic_status("IJ789KL"), "light traffic")
    def test_proxy_driver_get_veichle_status(self):
        self.assertEqual(self.proxy_driver.get_vehicle_status("MN012OP"), 40)
    def test_proxy_driver_set_driver(self):
        self.assertEqual(self.proxy_driver.set_driver(101, "IJ789KL"), "Access denied")
        self.assertEqual(self.proxy_driver.get_vehicle_status("IJ789KL"), 305)
    def test_proxy_driver_set_delivery_route(self):
        self.assertEqual(self.proxy_driver.set_delivery_route("EF456GH", "Oak Lane → Industrial Park"),
                         "Access denied")
        self.assertEqual(self.proxy_driver.get_delivery_route("EF456GH"),
                         "Appia Street → Ring Road → Tuscolana Street")
    def test_proxy_admin_get_delivery_route(self):
        self.assertEqual(self.proxy_admin.get_delivery_route("AB123CD"),
                         "Nomentana Street → East Ring Road → Tiburtina Street")
    def test_proxy_admin_get_traffic_status(self):
        self.assertEqual(self.proxy_admin.get_traffic_status("IJ789KL"), "light traffic")
    def test_proxy_admin_get_vehicle_status(self):
        self.assertEqual(self.proxy_admin.get_vehicle_status("MN012OP"), 40)
    def test_proxy_admin_set_driver(self):
        self.assertEqual(self.proxy_admin.set_driver(101, "IJ789KL"), "Done")
        self.assertEqual(self.proxy_admin.get_vehicle_status("IJ789KL"), 101)
    def test_proxy_admin_set_delivery_route(self):
        self.assertEqual(self.proxy_admin.set_delivery_route("EF456GH", "Oak Lane → Industrial Park"),
                         "Done")
        self.assertEqual(self.proxy_admin.get_delivery_route("EF456GH"), "Oak Lane → Industrial Park")
    def test_proxy_unknown_get_delivery_route(self):
        self.assertEqual(self.proxy_unknown.get_delivery_route("AB123CD"), "Access denied")
    def test_proxy_unknown_get_vehicle_status(self):
        self.assertEqual(self.proxy_unknown.get_vehicle_status("MN012OP"), "Access denied")
    def test_proxy_unknown_get_traffic_status(self):
        self.assertEqual(self.proxy_unknown.get_traffic_status("IJ789KL"), "Access denied")
    def test_proxy_unknown_set_driver(self):
        self.assertEqual(self.proxy_unknown.set_driver(101, "IJ789KL"), "Access denied")
    def test_proxy_unknown_set_delivery_route(self):
        self.assertEqual(self.proxy_unknown.set_delivery_route("EF456GH", "Oak Lane → Industrial Park"),
                         "Access denied")