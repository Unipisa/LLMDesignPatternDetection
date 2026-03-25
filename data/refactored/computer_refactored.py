from abc import ABC, abstractmethod
import pprint

# builder for 3 different computers: surface, macbook, desktop

# products' interface
class Computer(ABC):
    def __init__(self):
        self.parts={
            "core": None,
            "storage": None,
            "display": None,
            "graphics": None,
            "chassis": None,
        }
    def add_part(self, part, value):
        self.parts[part] = value
    @abstractmethod
    def __str__(self):
        pass


# concrete products
class Surface(Computer):
    def __str__(self):
        return "Surface computer: " + str(self.parts)

class Macbook(Computer):
    def __str__(self):
        return "Macbook computer: " + str(self.parts)

class Desktop(Computer):
    def __str__(self):
        return "Desktop computer: " + str(self.parts)

# abstract builder interface
class ComputerBuilder(ABC):
    @abstractmethod
    def build_core(self):
        pass
    @abstractmethod
    def build_storage(self):
        pass
    @abstractmethod
    def build_display(self):
        pass
    @abstractmethod
    def build_graphics(self):
        pass
    @abstractmethod
    def build_chassis(self):
        pass

# concrete builders
class MacbookBuilder(ComputerBuilder):
    def __init__(self):
        self._product = None
        self.reset()
    def reset(self):
        self._product = Macbook()
    def build_core(self):
        self._product.add_part("core", "Apple M3 Max (16-core CPU, 64GB Unified Memory)")
    def build_storage(self):
        self._product.add_part("storage", "2TB NVMe Onboard SSD")
    def build_display(self):
        self._product.add_part("display", "16.2-inch Liquid Retina XDR display (Mini-LED, 120Hz ProMotion)")
    def build_graphics(self):
        self._product.add_part("graphics", "Apple 40-core GPU (Integrated)")
    def build_chassis(self):
        self._product.add_part("chassis", "Space Gray Aluminum Unibody, 100Wh Battery, Active Dual-Fan Cooling")
    def get_product(self):
        product = self._product
        self.reset()
        return product

class DesktopBuilder(ComputerBuilder):
    def __init__(self):
        self._product = None
        self.reset()
    def reset(self):
        self._product = Desktop()
    def build_core(self):
        self._product.add_part("core", "Intel Core i9-11900H (16-core CPU, 32GB DDR4)")
    def build_storage(self):
        self._product.add_part("storage", "1TB NVMe Onboard SSD")
    def build_display(self):
        self._product.add_part("display", "15.6-inch QHD (Iris) Display (1ms Refresh Rate)")
    def build_graphics(self):
        self._product.add_part("graphics", "NVIDIA GeForce RTX 3080 (12GB GDDR6X)")
    def build_chassis(self):
        self._product.add_part("chassis", "Mid-tower case with optimized airflow, RGB lighting, 1000W PSU, Liquid Cooling System")
    def get_product(self):
        product = self._product
        self.reset()
        return product

class SurfaceBuilder(ComputerBuilder):
    def __init__(self):
        self._product = None
        self.reset()
    def reset(self):
        self._product = Surface()
    def build_core(self):
        self._product.add_part("core", "Snapdragon X Elite (12-core CPU, 16GB LPDDR5x RAM)")
    def build_storage(self):
        self._product.add_part("storage", "512GB Removable SSD")
    def build_display(self):
        self._product.add_part("display", "13-inch PixelSense Flow display (OLED, Touchscreen, 120Hz)")
    def build_graphics(self):
        self._product.add_part("graphics", "Qualcomm Adreno GPU (Integrated)")
    def build_chassis(self):
        self._product.add_part("chassis", "Anodized Aluminum casing with Kickstand, Magnetic Keyboard connector, Passive Cooling")
    def get_product(self):
        product = self._product
        self.reset()
        return product

# director
class Director:
    def __init__(self, builder):
        self._builder = builder
    def change_builder(self, builder):
        self._builder = builder
    def make(self):
        self._builder.build_core()
        self._builder.build_storage()
        self._builder.build_display()
        self._builder.build_graphics()
        self._builder.build_chassis()

def client():
    macbook_builder = MacbookBuilder()
    director= Director(macbook_builder)
    director.make()
    print(macbook_builder.get_product())
    print("--------------------")
    desktop_builder = DesktopBuilder()
    director.change_builder(desktop_builder)
    director.make()
    print(desktop_builder.get_product())
    print("--------------------")
    surface_builder = SurfaceBuilder()
    director.change_builder(surface_builder)
    director.make()
    print(surface_builder.get_product())
