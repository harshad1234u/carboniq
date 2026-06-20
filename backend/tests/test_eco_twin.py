from services.eco_twin_service import calculate_eco_twin
from models.ai_coach import Recommendation


def test_basic_prediction():
    """ """
    recs = [
        Recommendation(
            title="T1",
            description="D1",
            co2_savings_kg=50,
            cost_savings_inr=100,
            difficulty="easy",
        )
    ]
    res = calculate_eco_twin(200, recs)
    assert res.predicted_footprint == 150
    assert res.reduction_percentage == 25.0


def test_zero_savings():
    """ """
    res = calculate_eco_twin(200, [])
    assert res.predicted_footprint == 200
    assert res.reduction_percentage == 0.0


def test_prediction_never_negative():
    """ """
    recs = [
        Recommendation(
            title="T1",
            description="D1",
            co2_savings_kg=300,
            cost_savings_inr=100,
            difficulty="easy",
        )
    ]
    res = calculate_eco_twin(200, recs)
    assert res.predicted_footprint == 0
    assert res.reduction_percentage == 100.0
