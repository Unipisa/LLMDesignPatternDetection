from abc import ABC, abstractmethod

# Implementation with factory method

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

class House:
    def __init__(self, furniture, garden, alarm):
        self.furniture = furniture
        self.garden = garden
        self.alarm = alarm
    def describe(self):
        return self.furniture.get_style(), self.garden.get_description(), self.alarm.get_defense()

class HouseCreator(ABC):
    @abstractmethod
    def create_house(self):
        pass

class ApartmentCreator(HouseCreator):
    def create_house(self):
        return House(ModernFurniture(), NoneGarden(), NoneAlarm())

class TownHouseCreator(HouseCreator):
    def create_house(self):
        return House(ClassicFurniture(), NoneGarden(), VideoMonitoredAlarm())

class VillaCreator(HouseCreator):
    def create_house(self):
        return House(RusticFurniture(), FlowerGarden(), PrivateSecurityAlarm())