from enum import Enum

class Brand(Enum):
    SAMSUNG = 1
    PHILIPS = 2

class Box:
    def __init__(self, brand: Brand):
        self.brand = brand

    def get_tv_description(self):
        if self.brand == Brand.SAMSUNG:
            return "Samsung TV"
        elif self.brand == Brand.PHILIPS:
            return "Philips TV"
        return None

    def get_rc_description(self):
        if self.brand == Brand.SAMSUNG:
            return "Samsung RC"
        elif self.brand == Brand.PHILIPS:
            return "Philips RC"
        return None
