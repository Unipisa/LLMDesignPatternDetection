from abc import ABC, abstractmethod

# CONCRETE PRODUCTS:
# There are 3 types of house furnitures: modern, classic, rustic.
# There are 2 types of house gardens: none, flowers
# There are 4 types of alarms: none, siren, video-monitored, private-security

# FAMILIES (concrete factories according to an abstract factory pattern):
# There are 3 different houses coming with complete pack (fornituyre, alarm and alarm):
# 1. Apartment: modern furniture, none garden, none alarm
# 2. TownHouse: classic furniture, none garden, video-monitored alarm
# 3. Villa: rustic furniture, flower garden, private-security alarm

# abstract products
class Furniture(ABC):
    @abstractmethod
    def get_style(self):
        pass

class Garden(ABC):
    @abstractmethod
    def get_description(self):
        pass

class Alarm(ABC):
    @abstractmethod
    def get_defense(self):
        pass

# concrete products
class ModernFurniture(Furniture):
    def get_style(self):
        return "Modern vibes only: clear lines, bold ideas!"

class ClassicFurniture(Furniture):
    def get_style(self):
        return "Classic is old-fashioned, but still fresh."

class RusticFurniture(Furniture):
    def get_style(self):
        return "Wood, stone and heart: that's rustic style!"

class NoneGarden(Garden):
    def get_description(self):
        return "No garden, no problem!"

class FlowerGarden(Garden):
    def get_description(self):
        return "Flowers, flowers everywhere!"

class NoneAlarm(Alarm):
    def get_defense(self):
        return "No alarm, just peace and quiet."

class SirenAlarm(Alarm):
    def get_defense(self):
        return "Siren, siren, siren..."

class VideoMonitoredAlarm(Alarm):
    def get_defense(self):
        return "Video-monitoring alarm: smile, you are on camera!"

class PrivateSecurityAlarm(Alarm):
    def get_defense(self):
        return "Private security in action."

# abstract factory
class House(ABC):
    @abstractmethod
    def create_furniture(self):
        pass
    @abstractmethod
    def create_garden(self):
        pass
    @abstractmethod
    def create_alarm(self):
        pass


# concrete factories
class Apartment(House):
    def create_furniture(self):
        return ModernFurniture()
    def create_garden(self):
        return NoneGarden()
    def create_alarm(self):
        return NoneAlarm()

class TownHouse(House):
    def create_furniture(self):
        return ClassicFurniture()
    def create_garden(self):
        return NoneGarden()
    def create_alarm(self):
        return VideoMonitoredAlarm()

class Villa(House):
    def create_furniture(self):
        return RusticFurniture()
    def create_garden(self):
        return FlowerGarden()
    def create_alarm(self):
        return PrivateSecurityAlarm()

def client(house: House):
    furniture = house.create_furniture()
    garden = house.create_garden()
    alarm = house.create_alarm()
    print(f"I finally finalized the purchase of my new house! Here it's a brief description:\n"
          f"{furniture.get_style()} "
          f"{garden.get_description()} "
          f"{alarm.get_defense()}")


