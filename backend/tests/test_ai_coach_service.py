import pytest
from services.ai_coach_service import (
    get_recommendations,
    _select_fallback_recommendations,
)
from models.calculator import CarbonResult, CarbonScore
from models.weather import WeatherData
from utils.config import settings


@pytest.fixture(autouse=True)
def setup_ai_coach_test():
    original_key = settings.gemini_api_key
    object.__setattr__(settings, "gemini_api_key", "fake_key")
    yield
    object.__setattr__(settings, "gemini_api_key", original_key)


def _get_mock_footprint():
    return CarbonResult(
        transport_emissions=100.0,
        electricity_emissions=200.0,  # Highest
        food_emissions=50.0,
        flight_emissions=0.0,
        total_emissions=350.0,
        carbon_score=CarbonScore(score=80, level="Eco Aware", color="#4CAF50"),
    )


@pytest.mark.asyncio
async def test_fallback_recommendations_no_key():
    object.__setattr__(settings, "gemini_api_key", "")
    footprint = _get_mock_footprint()
    response = await get_recommendations(footprint, None, {})
    assert len(response.recommendations) == 3
    # Electricity is highest, so the first rec should relate to electricity
    assert (
        "AC" in response.recommendations[0].title
        or "LED" in response.recommendations[0].title
        or "Appliances" in response.recommendations[0].title
    )


@pytest.mark.asyncio
async def test_fallback_recommendations_exception(mocker):
    mocker.patch(
        "services.ai_coach_service._call_gemini", side_effect=Exception("API Down")
    )
    footprint = _get_mock_footprint()
    response = await get_recommendations(footprint, None, {})
    assert len(response.recommendations) == 3


@pytest.mark.asyncio
async def test_gemini_success(mocker):
    footprint = _get_mock_footprint()
    from models.ai_coach import Recommendation

    mock_recs = [
        Recommendation(
            title="Test",
            description="Test Desc",
            co2_savings_kg=10,
            cost_savings_inr=100,
            difficulty="easy",
        ),
        Recommendation(
            title="Test 2",
            description="Test Desc 2",
            co2_savings_kg=20,
            cost_savings_inr=200,
            difficulty="medium",
        ),
        Recommendation(
            title="Test 3",
            description="Test Desc 3",
            co2_savings_kg=30,
            cost_savings_inr=300,
            difficulty="hard",
        ),
    ]
    mocker.patch("services.ai_coach_service._call_gemini", return_value=mock_recs)
    response = await get_recommendations(footprint, None, {})
    assert len(response.recommendations) == 3
    assert response.total_co2_savings == 60.0
    assert response.total_cost_savings == 600.0
