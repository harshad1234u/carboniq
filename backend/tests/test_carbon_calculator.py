import pytest
from services.carbon_calculator import calculate_emissions, calculate_carbon_score
from models.calculator import CarbonInput


def test_car_petrol_emissions(base_input):
    """

    Args:
      base_input: 

    Returns:

    """
    base_input.vehicle_type = "car_petrol"
    base_input.daily_travel_km = 10
    result = calculate_emissions(base_input)
    assert result.transport_emissions == pytest.approx(10 * 30 * 0.21)


def test_car_electric_emissions(base_input):
    """

    Args:
      base_input: 

    Returns:

    """
    base_input.vehicle_type = "car_electric"
    base_input.daily_travel_km = 10
    result = calculate_emissions(base_input)
    assert result.transport_emissions == pytest.approx(10 * 30 * 0.05)


def test_bicycle_zero_emissions(base_input):
    """

    Args:
      base_input: 

    Returns:

    """
    base_input.vehicle_type = "bicycle"
    base_input.daily_travel_km = 10
    result = calculate_emissions(base_input)
    assert result.transport_emissions == 0


def test_all_diet_types(base_input):
    """

    Args:
      base_input: 

    Returns:

    """
    diets = {"meat_heavy": 3.3, "average": 2.5, "vegetarian": 1.7, "vegan": 1.5}
    for diet, factor in diets.items():
        base_input.diet_type = diet
        result = calculate_emissions(base_input)
        assert result.food_emissions == pytest.approx(factor * 30)


def test_flight_emissions_calculation(base_input):
    """

    Args:
      base_input: 

    Returns:

    """
    base_input.flights_short = 2
    base_input.flights_long = 1
    result = calculate_emissions(base_input)
    expected = 134.17
    assert result.flight_emissions == pytest.approx(expected)


def test_total_emissions_sum(base_input):
    """

    Args:
      base_input: 

    Returns:

    """
    base_input.vehicle_type = "car_petrol"
    base_input.daily_travel_km = 10  # 63
    base_input.electricity_kwh = 100  # 82
    base_input.ac_hours = 2  # 1.5 * 0.82 * 2 * 30 = 73.8
    base_input.diet_type = "vegan"  # 1.5 * 30 = 45
    base_input.flights_short = 1  # 255 / 12 = 21.25
    result = calculate_emissions(base_input)

    assert result.transport_emissions == 63
    assert result.electricity_emissions == 155.8  # 82 + 73.8
    assert result.food_emissions == 45
    assert result.flight_emissions == 21.25
    assert result.total_emissions == 63 + 155.8 + 45 + 21.25


def test_carbon_score_boundaries():
    """ """
    assert calculate_carbon_score(0).level == "Green Hero"
    assert calculate_carbon_score(150).level == "Eco Aware"
    assert calculate_carbon_score(250).level == "High Impact"
    assert calculate_carbon_score(334).level == "Critical"
