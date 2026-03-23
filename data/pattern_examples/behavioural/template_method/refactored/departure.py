from abc import ABC, abstractmethod
from enum import Enum
# applying template method to model a veichle departure


# weather values
class Weather(Enum):
    RAINY = 1
    SUNNY = 2
    CLOUDY = 3
    WINDY = 4

class LandingGearConditions(Enum):
    GOOD = 1
    MEDIUM = 2
    BAD = 3

# abstract departure class
class Departure(ABC):
    def __init__(self, id_document = None):
        self.id_document = id_document    # document to be verified for driver/ pilot
    def check_documents(self):
        if self.id_document is None:
            return True
        print(f"Verifying documents: {self.id_document}")
        # simple check for the document
        return len([c for c in self.id_document if 'A'<=c<='Z'])==5 and self.id_document[-1].isdigit()

    def check_fuel(self):
        return True
    @abstractmethod
    def check_tires(self):
        pass
    def extra_checks(self):
        return True
    def depart(self):
        # template method
        if self.check_documents() and self.check_fuel() and self.check_tires() and self.extra_checks():
            return "Departing"
        else:
            return "Not departing"

# concrete departure classes
class CarDeparture(Departure):
    def __init__(self, id_document, tire1, tire2, tire3, tire4, fuel_level):
        super().__init__(id_document)

        # binding tires pressure parameters (unit of mesure is in bar)
        self.tire1 = tire1
        self.tire2 = tire2
        self.tire3 = tire3
        self.tire4 = tire4
        self.fuel_level = fuel_level
    def check_fuel(self):
        print(f"Checking fuel level")
        return self.fuel_level > 30     # fuel_level is in liters
    def check_tires(self):
        print(f"Checking tires")
        return sum([self.tire1, self.tire2, self.tire3, self.tire4]) /4 > 2


class FlightsDeparture(Departure):
    def __init__(self, id_document, landing_gear_condition: LandingGearConditions, weather: Weather, fuel_level):
        super().__init__(id_document)
        self.landing_gear_condition = landing_gear_condition
        self.weather = weather
        self.fuel_level = fuel_level

    def check_fuel(self):
        print(f"Checking fuel level")
        return self.fuel_level >=10000
    def check_tires(self):
        print(f"Checking tires")
        return self.landing_gear_condition == LandingGearConditions.GOOD
    def extra_checks(self):
        print(f"Checking weather")
        return self.weather != Weather.WINDY

class Bike(Departure):
    def __init__(self, tire1, tire2, id_document = None):
        super().__init__(id_document)
        self.tire1 = tire1
        self.tire2 = tire2
    def check_tires(self):
        print(f"Checking tires")
        return self.tire1 >= 1.5 and self.tire2 >= 1.5

def client():
    departure = FlightsDeparture(id_document="ABCDE1", landing_gear_condition=LandingGearConditions.GOOD,
                                 weather=Weather.SUNNY, fuel_level=10000)
    print(departure.depart())
    print("-----------------------------------")
    departure = Bike(tire1=1.5, tire2=1.5)
    print(departure.depart())
    print("-----------------------------------")
    departure = CarDeparture(id_document="ABCDE1", tire1=0, tire2=1.5, tire3=1.5, tire4=1.5, fuel_level=50)
    print(departure.depart())

