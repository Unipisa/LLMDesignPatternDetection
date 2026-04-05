from enum import Enum

class ModernFurniture:
    def get_style(self):
        return "Modern vibes only: clear lines, bold ideas!"

class ClassicFurniture:
    def get_style(self):
        return "Classic is old-fashioned, but still fresh."

class RusticFurniture:
    def get_style(self):
        return "Wood, stone and heart: that's rustic style!"

class NoneGarden:
    def get_description(self):
        return "No garden, no problem!"

class FlowerGarden:
    def get_description(self):
        return "Flowers, flowers everywhere!"

class NoneAlarm:
    def get_defense(self):
        return "No alarm, just peace and quiet."

class SirenAlarm:
    def get_defense(self):
        return "Siren, siren, siren..."

class VideoMonitoredAlarm:
    def get_defense(self):
        return "Video-monitoring alarm: smile, you are on camera!"

class PrivateSecurityAlarm:
    def get_defense(self):
        return "Private security in action."

class HouseType(Enum):
    APARTMENT = "Apartment"
    TOWNHOUSE = "Townhouse"
    VILLA = "Villa"

class House:
    def __init__(self, house_type: HouseType):
        self.house_type = house_type

    def describe(self):
        if self.house_type == HouseType.APARTMENT:
            return ModernFurniture().get_style(), NoneGarden().get_description(), NoneAlarm().get_defense()
        elif self.house_type == HouseType.TOWNHOUSE:
            return ClassicFurniture().get_style(), NoneGarden().get_description(), VideoMonitoredAlarm().get_defense()
        elif self.house_type == HouseType.VILLA:
            return RusticFurniture().get_style(), FlowerGarden().get_description(), PrivateSecurityAlarm().get_defense()
        return None, None, None


