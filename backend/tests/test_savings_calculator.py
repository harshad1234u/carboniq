from services.savings_calculator_service import calculate_savings
from models.ai_coach import Recommendation


def test_transport_savings():
    recs = [
        Recommendation(
            title="Car to Bus",
            description="Use public transport",
            co2_savings_kg=0,
            cost_savings_inr=0,
            difficulty="easy",
        )
    ]
    res = calculate_savings(
        recs, 100, {"transport_type": "car_petrol", "avg_travel_distance": 10}
    )
    # Since mock service uses basic logic, we check if it populates the cost savings
    assert len(res) == 1
    assert res[0]["cost_savings_inr"] > 0


def test_zero_footprint():
    recs = [
        Recommendation(
            title="Reduce AC",
            description="Use fan",
            co2_savings_kg=0,
            cost_savings_inr=0,
            difficulty="easy",
        )
    ]
    res = calculate_savings(recs, 0, {})
    assert res[0]["cost_savings_inr"] == 720.0


def test_savings_never_negative():
    recs = [
        Recommendation(
            title="Eat more meat",
            description="Not eco",
            co2_savings_kg=0,
            cost_savings_inr=0,
            difficulty="hard",
        )
    ]
    res = calculate_savings(recs, 100, {})
    for r in res:
        assert r["cost_savings_inr"] >= 0
