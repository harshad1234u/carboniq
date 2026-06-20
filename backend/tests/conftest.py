import pytest
from models.calculator import CarbonInput


@pytest.fixture
def base_input():
    """ """
    return CarbonInput(
        vehicle_type="bicycle",
        daily_travel_km=0,
        electricity_kwh=0,
        ac_hours=0,
        diet_type="average",
        flights_short=0,
        flights_long=0,
    )
