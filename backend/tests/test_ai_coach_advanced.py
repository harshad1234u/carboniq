"""Tests for AI Coach prompt building and additional edge cases."""
import pytest
from unittest.mock import patch, AsyncMock
from services.ai_coach_service import (
    _build_prompt,
    _select_fallback_recommendations,
    get_recommendations,
)
from models.calculator import CarbonResult, CarbonScore
from models.weather import WeatherData
from utils.config import settings


def _make_footprint(**overrides):
    defaults = dict(
        transport_emissions=100.0,
        electricity_emissions=200.0,
        food_emissions=50.0,
        flight_emissions=0.0,
        total_emissions=350.0,
        carbon_score=CarbonScore(score=80, level="Eco Aware", color="#4CAF50"),
    )
    defaults.update(overrides)
    return CarbonResult(**defaults)


# ---------------------------------------------------------------------------
# _build_prompt
# ---------------------------------------------------------------------------

class TestBuildPrompt:
    def test_includes_footprint_data(self):
        fp = _make_footprint()
        prompt = _build_prompt(fp, None, {"city": "Mumbai"})
        assert "200.0" in prompt  # electricity_emissions
        assert "350.0" in prompt  # total_emissions
        assert "Mumbai" in prompt

    def test_includes_weather_context(self):
        fp = _make_footprint()
        weather = WeatherData(city="Delhi", temperature=42.0, description="Clear sky", humidity=30, icon="01d")
        prompt = _build_prompt(fp, weather, {})
        assert "Delhi" in prompt
        assert "42.0" in prompt
        assert "Clear sky" in prompt

    def test_handles_no_weather(self):
        fp = _make_footprint()
        prompt = _build_prompt(fp, None, {})
        assert "JSON" in prompt  # Still contains JSON format instructions

    def test_includes_profile_data(self):
        fp = _make_footprint()
        profile = {"city": "Pune", "transport_type": "car_petrol", "diet_type": "vegan", "household_size": 3}
        prompt = _build_prompt(fp, None, profile)
        assert "Pune" in prompt
        assert "car_petrol" in prompt
        assert "vegan" in prompt

    def test_handles_empty_profile(self):
        fp = _make_footprint()
        prompt = _build_prompt(fp, None, {})
        assert "Unknown" in prompt  # Defaults


# ---------------------------------------------------------------------------
# _select_fallback_recommendations  (more detailed tests)
# ---------------------------------------------------------------------------

class TestFallbackSelection:
    def test_transport_highest_gives_transport_recs(self):
        fp = _make_footprint(
            transport_emissions=500.0,
            electricity_emissions=50.0,
            food_emissions=30.0,
            flight_emissions=0.0,
            total_emissions=580.0,
        )
        recs = _select_fallback_recommendations(fp)
        assert len(recs) == 3
        # First rec should be transport-related
        assert any(kw in recs[0].title.lower() for kw in ["transport", "walk", "carpool", "cycle", "drive"])

    def test_food_highest_gives_food_recs(self):
        fp = _make_footprint(
            transport_emissions=10.0,
            electricity_emissions=10.0,
            food_emissions=500.0,
            flight_emissions=0.0,
            total_emissions=520.0,
        )
        recs = _select_fallback_recommendations(fp)
        assert len(recs) == 3
        food_keywords = ["meat", "vegetarian", "food", "waste", "lunch", "cook"]
        assert any(kw in recs[0].title.lower() for kw in food_keywords)

    def test_flights_highest_gives_flight_rec(self):
        fp = _make_footprint(
            transport_emissions=10.0,
            electricity_emissions=10.0,
            food_emissions=10.0,
            flight_emissions=500.0,
            total_emissions=530.0,
        )
        recs = _select_fallback_recommendations(fp)
        assert len(recs) == 3
        assert any("flight" in r.title.lower() or "train" in r.title.lower() for r in recs)

    def test_all_zero_emissions_still_returns_3(self):
        fp = _make_footprint(
            transport_emissions=0.0,
            electricity_emissions=0.0,
            food_emissions=0.0,
            flight_emissions=0.0,
            total_emissions=0.0,
        )
        recs = _select_fallback_recommendations(fp)
        assert len(recs) == 3

    def test_recommendations_have_positive_savings(self):
        fp = _make_footprint()
        recs = _select_fallback_recommendations(fp)
        for r in recs:
            assert r.co2_savings_kg > 0
            assert r.cost_savings_inr >= 0

    def test_recommendations_have_valid_difficulty(self):
        fp = _make_footprint()
        recs = _select_fallback_recommendations(fp)
        for r in recs:
            assert r.difficulty in ("easy", "medium", "hard")


# ---------------------------------------------------------------------------
# get_recommendations integration
# ---------------------------------------------------------------------------

class TestGetRecommendationsIntegration:
    @pytest.mark.asyncio
    async def test_with_weather_context(self):
        original = settings.gemini_api_key
        object.__setattr__(settings, 'gemini_api_key', '')
        try:
            fp = _make_footprint()
            weather = WeatherData(city="Chennai", temperature=35.0, description="Hot", humidity=80, icon="01d")
            resp = await get_recommendations(fp, weather, {"city": "Chennai"})
            assert len(resp.recommendations) == 3
            assert resp.weather_context == weather
        finally:
            object.__setattr__(settings, 'gemini_api_key', original)

    @pytest.mark.asyncio
    async def test_savings_totals_are_correct(self):
        original = settings.gemini_api_key
        object.__setattr__(settings, 'gemini_api_key', '')
        try:
            fp = _make_footprint()
            resp = await get_recommendations(fp, None, {})
            expected_co2 = round(sum(r.co2_savings_kg for r in resp.recommendations), 2)
            expected_cost = round(sum(r.cost_savings_inr for r in resp.recommendations), 2)
            assert resp.total_co2_savings == expected_co2
            assert resp.total_cost_savings == expected_cost
        finally:
            object.__setattr__(settings, 'gemini_api_key', original)
