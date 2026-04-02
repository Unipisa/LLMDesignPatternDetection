from data.baseline.computer_baseline import *
import unittest

class TestComputer (unittest.TestCase):
    def setUp(self):
        self.macbook = Computer(ComputerType.MACBOOK)
        self.surface = Computer(ComputerType.SURFACE)
        self.desktop = Computer(ComputerType.DESKTOP)

    def test_macbook_core(self):
        self.assertEqual(self.macbook.parts["core"], "Apple M3 Max (16-core CPU, 64GB Unified Memory)")

    def test_macbook_storage(self):
        self.assertEqual(self.macbook.parts["storage"], "2TB NVMe Onboard SSD")

    def test_macbook_display(self):
        self.assertEqual(self.macbook.parts["display"], "16.2-inch Liquid Retina XDR display (Mini-LED, 120Hz "
                                                        "ProMotion)")

    def test_macbook_graphics(self):
        self.assertEqual(self.macbook.parts["graphics"], "Apple 40-core GPU (Integrated)")

    def test_macbook_chassis(self):
        self.assertEqual(self.macbook.parts["chassis"], "Space Gray Aluminum Unibody, 100Wh Battery, Active "
                                                        "Dual-Fan Cooling")

    def test_desktop_core(self):
        self.assertEqual(self.desktop.parts["core"], "Intel Core i9-11900H (16-core CPU, 32GB DDR4)")

    def test_desktop_storage(self):
        self.assertEqual(self.desktop.parts["storage"], "1TB NVMe Onboard SSD")

    def test_desktop_display(self):
        self.assertEqual(self.desktop.parts["display"], "15.6-inch QHD (Iris) Display (1ms Refresh Rate)")

    def test_desktop_graphics(self):
        self.assertEqual(self.desktop.parts["graphics"], "NVIDIA GeForce RTX 3080 (12GB GDDR6X)")

    def test_desktop_chassis(self):
        self.assertEqual(self.desktop.parts["chassis"], "Mid-tower case with optimized airflow, RGB lighting, "
                                                        "1000W PSU, Liquid Cooling System")

    def test_surface_core(self):
        self.assertEqual(self.surface.parts["core"], "Snapdragon X Elite (12-core CPU, 16GB LPDDR5x RAM)")

    def test_surface_storage(self):
        self.assertEqual(self.surface.parts["storage"], "512GB Removable SSD")

    def test_surface_display(self):
        self.assertEqual(self.surface.parts["display"], "13-inch PixelSense Flow display (OLED, Touchscreen, "
                                                        "120Hz)")

    def test_surface_graphics(self):
        self.assertEqual(self.surface.parts["graphics"], "Qualcomm Adreno GPU (Integrated)")

    def test_surface_chassis(self):
        self.assertEqual(self.surface.parts["chassis"], "Anodized Aluminum casing with Kickstand, Magnetic "
                                                        "Keyboard connector, Passive Cooling")