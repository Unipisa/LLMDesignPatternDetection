from data.refactored.car_refactored_af import *
import unittest, pytest

class TestCar(unittest.TestCase):
    def setUp(self):
        self.sports_car_factory = SportsCarFactory()
        self.economy_car_factory = EconomyCarFactory()
        self.sports_car = Car(self.sports_car_factory.create_engine(), self.sports_car_factory.create_tank())
        self.economy_car = Car(self.economy_car_factory.create_engine(), self.economy_car_factory.create_tank())

    def test_sports_car_creation(self):
        assert isinstance(self.sports_car.engine, SportsEngine)
        assert isinstance(self.sports_car.tank, SportsTank)
        assert self.sports_car.engine.speed == 250
        assert self.sports_car.engine.fuel_consumption_per_km == 0.2
        assert self.sports_car.tank.capacity == 50
        assert self.sports_car.tank.fuel == 50

    def test_economy_car_creation(self):
        assert isinstance(self.economy_car.engine, EconomyEngine)
        assert isinstance(self.economy_car.tank, EconomyTank)
        assert self.economy_car.engine.speed == 120
        assert self.economy_car.engine.fuel_consumption_per_km == 0.05
        assert self.economy_car.tank.capacity == 40
        assert self.economy_car.tank.fuel == 40

    def test_car_travel_within_fuel_range(self):
        self.sports_car.travel(100)  # should consume 20L
        assert self.sports_car.check_kms() == 100
        assert self.sports_car.tank.fuel == 30

    def test_car_travel_exceeding_fuel_range(self):
        self.economy_car.travel(1000)  # requires 50L, but has only 40L
        assert self.economy_car.check_kms() == 0
        assert self.economy_car.tank.fuel == 40  # unchanged

    def test_car_refill(self):
        self.economy_car.travel(200)  # uses 10L
        assert self.economy_car.tank.fuel == 30

        self.economy_car.tank.refill()
        assert self.economy_car.tank.fuel == 40

    def test_multiple_travels_accumulate_distance(self):
        self.sports_car.travel(50)
        self.sports_car.travel(100)
        assert self.sports_car.check_kms() == 150

    # -------------------------
    # Edge Case Tests
    # -------------------------

    def test_zero_distance_travel(self):
        initial_fuel = self.sports_car.tank.fuel
        self.sports_car.travel(0)
        assert self.sports_car.check_kms() == 0
        assert self.sports_car.tank.fuel == initial_fuel  # no fuel used

    def test_travel_exact_fuel_limit(self):
        max_distance = self.economy_car.tank.fuel / self.economy_car.engine.fuel_consumption_per_km  # 40 / 0.05 = 800
        self.economy_car.travel(max_distance)
        assert pytest.approx(self.economy_car.check_kms()) == 800
        assert pytest.approx(self.economy_car.tank.fuel) == 0

    def test_travel_with_zero_fuel(self):
        self.sports_car.tank.fuel = 0  # manually empty tank
        self.sports_car.travel(10)
        assert self.sports_car.check_kms() == 0
        assert self.sports_car.tank.fuel == 0

    def test_refill_after_empty_travel(self):
        self.economy_car.tank.fuel = 0
        self.economy_car.tank.refill()
        assert self.economy_car.tank.fuel == self.economy_car.tank.capacity

    def test_floating_point_precision_travel(self):
        self.economy_car.travel(0.1)  # should consume 0.005L
        assert pytest.approx(self.economy_car.tank.fuel, 0.0001) == 39.995

