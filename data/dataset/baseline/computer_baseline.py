from enum import Enum

class ComputerType(Enum):
    MACBOOK= 1
    SURFACE = 2
    DESKTOP = 3

class Computer:
    def __init__(self, t: ComputerType):
        self.parts: dict[str, str| None]={
            "core": None,
            "storage": None,
            "display": None,
            "graphics": None,
            "chassis": None,
        }
        self.type = t

        if self.type == ComputerType.MACBOOK:
            self.parts["core"] = "Apple M3 Max (16-core CPU, 64GB Unified Memory)"
            self.parts["storage"] = "2TB NVMe Onboard SSD"
            self.parts["display"] = "16.2-inch Liquid Retina XDR display (Mini-LED, 120Hz ProMotion)"
            self.parts["graphics"] = "Apple 40-core GPU (Integrated)"
            self.parts["chassis"] = "Space Gray Aluminum Unibody, 100Wh Battery, Active Dual-Fan Cooling"
        elif self.type == ComputerType.DESKTOP:
            self.parts["core"] = "Intel Core i9-11900H (16-core CPU, 32GB DDR4)"
            self.parts["storage"] = "1TB NVMe Onboard SSD"
            self.parts["display"] = "15.6-inch QHD (Iris) Display (1ms Refresh Rate)"
            self.parts["graphics"] = "NVIDIA GeForce RTX 3080 (12GB GDDR6X)"
            self.parts["chassis"] = ("Mid-tower case with optimized airflow, RGB lighting, 1000W PSU, Liquid Cooling"
                                     " System")
        elif self.type == ComputerType.SURFACE:
            self.parts["core"] = "Snapdragon X Elite (12-core CPU, 16GB LPDDR5x RAM)"
            self.parts["storage"] = "512GB Removable SSD"
            self.parts["display"] = "13-inch PixelSense Flow display (OLED, Touchscreen, 120Hz)"
            self.parts["graphics"] = "Qualcomm Adreno GPU (Integrated)"
            self.parts["chassis"] = ("Anodized Aluminum casing with Kickstand, Magnetic Keyboard connector, Passive "
                                     "Cooling")

    def __str__(self):
        if self.type == ComputerType.MACBOOK:
            return "Macbook computer: " + str(self.parts)
        elif self.type == ComputerType.DESKTOP:
            return "Desktop computer: " + str(self.parts)
        elif self.type == ComputerType.SURFACE:
            return "Surface computer: " + str(self.parts)
        return "Unknown"