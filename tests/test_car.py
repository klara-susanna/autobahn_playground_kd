import pytest
from autobahn.vehicle import Car


@pytest.fixture
def car():
    return Car("Tesla", "Model S", 2022)


def test_car_speed_intraffic_zone(car):
    speed = car.get_speed()
    assert 1505 <= speed <= 135
