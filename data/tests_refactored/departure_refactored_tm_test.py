import unittest
from data.refactored.departure_refactored_tm import (Weather, LandingGearConditions, CarDeparture, BikeDeparture,
                                                     FlightDeparture)

class TestDepartures(unittest.TestCase):
    def test_bike_departure_ok(self):
        departure = BikeDeparture(tire1=1.5, tire2=1.5)
        self.assertEqual(departure.depart(), "Departing")
    def test_bike_departure_not_ok(self):
        departure = BikeDeparture(tire1=1.5, tire2=1.4)
        self.assertEqual(departure.depart(), "Not departing")
    def test_car_departure_ok(self):
        departure = CarDeparture(id_document="ABCDE1", tire1=3, tire2=2, tire3=2.1, tire4=1.5, fuel_level=50)
        self.assertEqual(departure.depart(), "Departing")
    def test_car_departure_not_ok(self):
        departure = CarDeparture(id_document="ABCDE1", tire1=1.5, tire2=1.5, tire3=1.5, tire4=2, fuel_level=10)
        self.assertEqual(departure.depart(), "Not departing")
    def test_flight_departure_ok(self):
        departure = FlightDeparture(id_document="ABCDE1", landing_gear_condition=LandingGearConditions.GOOD,
                                     weather=Weather.SUNNY, fuel_level=10000)
        self.assertEqual(departure.depart(), "Departing")
    def test_flight_departure_not_ok(self):
        departure = FlightDeparture(id_document="ABCDE1", landing_gear_condition=LandingGearConditions.GOOD,
                                     weather=Weather.WINDY, fuel_level=10000)
        self.assertEqual(departure.depart(), "Not departing")

