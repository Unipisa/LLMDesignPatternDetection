import unittest
from data.refactored.computer_refactored import *

class TestComputerBuilder (unittest.TestCase):
    def setUp(self):
        self.macbook_builder = MacbookBuilder()
        self.surface_builder = SurfaceBuilder()
        self.desktop_builder = DesktopBuilder()
        self.director = Director(None)

    def test_macbook_builder_core(self):
        self.director.change_builder(self.macbook_builder)
        self.director.make()
        self.assertEqual(self.macbook_builder.get_product().parts["core"], "Apple M3 Max (16-core CPU, "
                                                                           "64GB Unified Memory)")

    def test_macbook_builder_storage(self):
        self.director.change_builder(self.macbook_builder)
        self.director.make()
        self.assertEqual(self.macbook_builder.get_product().parts["storage"], "2TB NVMe Onboard SSD")

    def test_macbook_builder_display(self):
        self.director.change_builder(self.macbook_builder)
        self.director.make()
        self.assertEqual(self.macbook_builder.get_product().parts["display"], "16.2-inch Liquid Retina XDR "
                                                                              "display (Mini-LED, 120Hz ProMotion)")
    def test_macbook_builder_graphics(self):
        self.director.change_builder(self.macbook_builder)
        self.director.make()
        self.assertEqual(self.macbook_builder.get_product().parts["graphics"], "Apple 40-core GPU (Integrated)")

    def test_macbook_builder_chassis(self):
        self.director.change_builder(self.macbook_builder)
        self.director.make()
        self.assertEqual(self.macbook_builder.get_product().parts["chassis"], "Space Gray Aluminum Unibody, "
                                                                               "100Wh Battery, Active Dual-Fan Cooling")

    def test_desktop_builder_core(self):
        self.director.change_builder(self.desktop_builder)
        self.director.make()
        self.assertEqual(self.desktop_builder.get_product().parts["core"], "Intel Core i9-11900H (16-core CPU, "
                                                                           "32GB DDR4)")

    def test_desktop_builder_storage(self):
        self.director.change_builder(self.desktop_builder)
        self.director.make()
        self.assertEqual(self.desktop_builder.get_product().parts["storage"], "1TB NVMe Onboard SSD")

    def test_desktop_builder_display(self):
        self.director.change_builder(self.desktop_builder)
        self.director.make()
        self.assertEqual(self.desktop_builder.get_product().parts["display"], "15.6-inch QHD (Iris) Display "
                                                                              "(1ms Refresh Rate)")

    def test_desktop_builder_graphics(self):
        self.director.change_builder(self.desktop_builder)
        self.director.make()
        self.assertEqual(self.desktop_builder.get_product().parts["graphics"], "NVIDIA GeForce RTX 3080 (12GB "
                                                                               "GDDR6X)")

    def test_desktop_builder_chassis(self):
        self.director.change_builder(self.desktop_builder)
        self.director.make()
        self.assertEqual(self.desktop_builder.get_product().parts["chassis"], "Mid-tower case with optimized "
                                                                              "airflow, RGB lighting, 1000W PSU, Liquid "
                                                                              "Cooling System")

    def test_surface_builder_core(self):
        self.director.change_builder(self.surface_builder)
        self.director.make()
        self.assertEqual(self.surface_builder.get_product().parts["core"], "Snapdragon X Elite (12-core CPU, "
                                                                           "16GB LPDDR5x RAM)")
    def test_surface_builder_storage(self):
        self.director.change_builder(self.surface_builder)
        self.director.make()
        self.assertEqual(self.surface_builder.get_product().parts["storage"], "512GB Removable SSD")

    def test_surface_builder_display(self):
        self.director.change_builder(self.surface_builder)
        self.director.make()
        self.assertEqual(self.surface_builder.get_product().parts["display"], "13-inch PixelSense Flow display "
                                                                              "(OLED, Touchscreen, 120Hz)")
    def test_surface_builder_graphics(self):
        self.director.change_builder(self.surface_builder)
        self.director.make()
        self.assertEqual(self.surface_builder.get_product().parts["graphics"], "Qualcomm Adreno GPU "
                                                                               "(Integrated)")

    def test_surface_builder_chassis(self):
        self.director.change_builder(self.surface_builder)
        self.director.make()
        self.assertEqual(self.surface_builder.get_product().parts["chassis"], "Anodized Aluminum casing with "
                                                                               "Kickstand, Magnetic Keyboard "
                                                                              "connector, Passive Cooling")