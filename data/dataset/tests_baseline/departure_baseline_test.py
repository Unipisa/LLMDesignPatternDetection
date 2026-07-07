import unittest
from data.dataset.baseline.departure_baseline import Weather, LandingGearConditions, Vehicle, Departure



class TestDepartures(unittest.TestCase):
    def test_bike_departure_ok(self):
        departure = Departure(tire1=1.5, tire2=2.5, vehicle=Vehicle.BIKE)
        self.assertEqual(departure.departure(), "Departing")
    def test_bike_departure_not_ok(self):
        departure = Departure(tire1=1.5, tire2=1.4, vehicle=Vehicle.BIKE)
        self.assertEqual(departure.departure(), "Not departing")
    def test_car_departure_ok(self):
        departure = Departure(id_document="ABCDE1", tire1=3, tire2=2, tire3=2.1, tire4=1.5, fuel_level=50,
                              vehicle=Vehicle.CAR)
        self.assertEqual(departure.departure(), "Departing")
    def test_car_departure_not_ok(self):
        departure = Departure(id_document="ABCDE1", tire1=1.5, tire2=1.5, tire3=1.5, tire4=2, fuel_level=10,
                              vehicle=Vehicle.CAR)
        self.assertEqual(departure.departure(), "Not departing")
    def test_flight_departure_ok(self):
        departure = Departure(id_document="ABCDE1", landing_gear_condition=LandingGearConditions.GOOD,
                              weather=Weather.SUNNY, fuel_level=10000, vehicle=Vehicle.FLIGHT)
        self.assertEqual(departure.departure(), "Departing")
    def test_flight_departure_not_ok(self):
        departure = Departure(id_document="ABCDE1", landing_gear_condition=LandingGearConditions.GOOD,
                              weather=Weather.WINDY, fuel_level=10000, vehicle=Vehicle.FLIGHT)
        self.assertEqual(departure.departure(), "Not departing")