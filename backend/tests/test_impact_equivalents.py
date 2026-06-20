from services.impact_equivalent_service import calculate_equivalents

def test_driving_km_conversion():
    res = calculate_equivalents(100)
    assert res["driving_km"] == 470.0

def test_smartphone_charges_conversion():
    res = calculate_equivalents(10)
    assert res["smartphone_charges"] == 1000.0

def test_trees_to_offset_conversion():
    res = calculate_equivalents(22)
    assert res["trees_to_offset"] == 1.0

def test_led_hours_conversion():
    res = calculate_equivalents(1)
    assert res["led_bulb_hours"] == 100.0

def test_zero_emissions():
    res = calculate_equivalents(0)
    assert res["driving_km"] == 0
    assert res["smartphone_charges"] == 0

def test_large_emissions():
    res = calculate_equivalents(1000)
    assert res["driving_km"] > 0
    assert res["trees_to_offset"] > 0
