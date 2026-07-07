from enum import Enum


class Weather(Enum):
    RAINY = 1
    SUNNY = 2
    CLOUDY = 3
    WINDY = 4

class LandingGearConditions(Enum):
    GOOD = 1
    MEDIUM = 2
    BAD = 3

class Vehicle(Enum):
    BIKE = 1
    CAR = 2
    FLIGHT = 3


class Departure:
    def __init__(self,  vehicle: Vehicle, id_document = None, tire1 = None, tire2 = None, tire3 = None, tire4 = None,
                 fuel_level = None, landing_gear_condition: LandingGearConditions = None, weather: Weather = None):
        self.id_document = id_document
        self.vehicle = vehicle
        self.tire1 = tire1
        self.tire2 = tire2
        self.tire3 = tire3
        self.tire4 = tire4
        self.fuel_level = fuel_level
        self.landing_gear_condition = landing_gear_condition
        self.weather = weather
    def departure(self):
        if self.vehicle == Vehicle.BIKE:
            print("Checking tires")
            if self.tire1 >= 1.5 and self.tire2 >= 1.5:
                return "Departing"
            return "Not departing"
        elif self.vehicle == Vehicle.CAR:
            print(f"Verifying documents: {self.id_document}")
            print(f"Checking fuel level")
            print(f"Checking tires")
            if (len([c for c in self.id_document if 'A'<=c<='Z'])==5 and self.id_document[-1].isdigit() and
                    self.fuel_level > 30 and sum([self.tire1, self.tire2, self.tire3, self.tire4]) /4 > 2):
                return "Departing"
            return "Not departing"
        elif self.vehicle == Vehicle.FLIGHT:
            print(f"Verifying documents: {self.id_document}")
            print(f"Checking fuel level")
            print(f"Checking tires")
            print(f"Checking weather")
            if (len([c for c in self.id_document if 'A'<=c<='Z'])==5 and self.id_document[-1].isdigit() and
                    self.fuel_level >=10000 and self.landing_gear_condition == LandingGearConditions.GOOD and
                    self.weather != Weather.WINDY):
                return "Departing"
            return "Not departing"
        return None
