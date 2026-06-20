"""Tests for Carbon API eco-twin and AI coach endpoints with full mocking."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=False)


class _FakeUser:
    """ """
    id = "test-user-uuid"


def _override_auth():
    """ """
    return _FakeUser()


@pytest.fixture(autouse=True)
def _patch_auth():
    """ """
    from api.profile import get_current_user

    app.dependency_overrides[get_current_user] = _override_auth
    yield
    app.dependency_overrides.clear()


_MOCK_ENTRY = {
    "id": "entry-uuid",
    "profile_id": "test-user-uuid",
    "transport_emissions": 100.0,
    "electricity_emissions": 200.0,
    "food_emissions": 50.0,
    "flight_emissions": 25.0,
    "total_emissions": 375.0,
    "carbon_score": 65,
    "carbon_level": "Eco Aware",
}

_MOCK_RECS = {
    "id": "rec-uuid",
    "profile_id": "test-user-uuid",
    "entry_id": "entry-uuid",
    "recommendations": [
        {
            "title": "Rec 1",
            "description": "Desc 1",
            "co2_savings_kg": 10.0,
            "cost_savings_inr": 100.0,
            "difficulty": "easy",
        },
        {
            "title": "Rec 2",
            "description": "Desc 2",
            "co2_savings_kg": 20.0,
            "cost_savings_inr": 200.0,
            "difficulty": "medium",
        },
        {
            "title": "Rec 3",
            "description": "Desc 3",
            "co2_savings_kg": 30.0,
            "cost_savings_inr": 300.0,
            "difficulty": "hard",
        },
    ],
}


class TestAiCoachEndpointFull:
    """ """
    @patch("api.carbon.RecommendationRepository")
    @patch("api.carbon.CarbonRepository")
    @patch("api.carbon.get_profile")
    @patch("api.carbon.get_weather", new_callable=AsyncMock)
    @patch("api.carbon.get_recommendations", new_callable=AsyncMock)
    def test_successful_ai_coach(
        self, mock_recs, mock_weather, mock_prof, mock_carbon, mock_rec_repo
    ):
        """

        Args:
          mock_recs: 
          mock_weather: 
          mock_prof: 
          mock_carbon: 
          mock_rec_repo: 

        Returns:

        """
        from models.ai_coach import Recommendation, AiCoachResponse
        from models.weather import WeatherData

        mock_prof.return_value = {
            "city": "Mumbai",
            "transport_type": "car_petrol",
            "diet_type": "average",
        }
        mock_carbon.get_latest.return_value = _MOCK_ENTRY
        mock_weather.return_value = WeatherData(
            city="Mumbai",
            temperature=30.0,
            description="Clear",
            humidity=60,
            icon="01d",
        )
        mock_recs.return_value = AiCoachResponse(
            recommendations=[
                Recommendation(
                    title="R1",
                    description="D1",
                    co2_savings_kg=10.0,
                    cost_savings_inr=100.0,
                    difficulty="easy",
                ),
                Recommendation(
                    title="R2",
                    description="D2",
                    co2_savings_kg=20.0,
                    cost_savings_inr=200.0,
                    difficulty="medium",
                ),
                Recommendation(
                    title="R3",
                    description="D3",
                    co2_savings_kg=30.0,
                    cost_savings_inr=300.0,
                    difficulty="hard",
                ),
            ],
            total_co2_savings=60.0,
            total_cost_savings=600.0,
            weather_context=None,
        )
        mock_rec_repo.create.return_value = {}

        resp = client.post("/api/carbon/ai-coach")
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["recommendations"]) == 3
        assert body["total_co2_savings"] == 60.0


class TestEcoTwinEndpoint:
    """ """
    @patch("api.carbon.EcoPredictionRepository")
    @patch("api.carbon.RecommendationRepository")
    @patch("api.carbon.CarbonRepository")
    def test_successful_eco_twin(self, mock_carbon, mock_rec_repo, mock_eco_repo):
        """

        Args:
          mock_carbon: 
          mock_rec_repo: 
          mock_eco_repo: 

        Returns:

        """
        mock_carbon.get_latest.return_value = _MOCK_ENTRY
        mock_rec_repo.get_latest.return_value = _MOCK_RECS
        mock_eco_repo.create.return_value = {}

        resp = client.post("/api/carbon/eco-twin", json={"entry_id": "entry-uuid"})
        assert resp.status_code == 200
        body = resp.json()
        assert "current_footprint" in body
        assert "predicted_footprint" in body
        assert body["current_footprint"] == 375.0
        assert body["predicted_footprint"] < 375.0

    @patch("api.carbon.RecommendationRepository")
    @patch("api.carbon.CarbonRepository")
    def test_no_carbon_entry(self, mock_carbon, mock_rec_repo):
        """

        Args:
          mock_carbon: 
          mock_rec_repo: 

        Returns:

        """
        mock_carbon.get_latest.return_value = None
        resp = client.post("/api/carbon/eco-twin", json={"entry_id": "entry-uuid"})
        assert resp.status_code == 400

    @patch("api.carbon.RecommendationRepository")
    @patch("api.carbon.CarbonRepository")
    def test_no_recommendations(self, mock_carbon, mock_rec_repo):
        """

        Args:
          mock_carbon: 
          mock_rec_repo: 

        Returns:

        """
        mock_carbon.get_latest.return_value = _MOCK_ENTRY
        mock_rec_repo.get_latest.return_value = None
        resp = client.post("/api/carbon/eco-twin", json={"entry_id": "entry-uuid"})
        assert resp.status_code == 400


class TestCalculateWithDbError:
    """ """
    @patch("api.carbon.CarbonRepository")
    def test_db_save_failure_returns_400(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.create_entry.side_effect = Exception("DB write failed")
        resp = client.post(
            "/api/carbon/calculate",
            json={
                "vehicle_type": "car_petrol",
                "daily_travel_km": 20,
                "electricity_kwh": 300,
                "ac_hours": 4,
                "diet_type": "average",
                "flights_short": 0,
                "flights_long": 0,
            },
        )
        assert resp.status_code == 400


class TestDashboardCompleteChallengeEndpoint:
    """ """
    @patch("api.dashboard.BadgeRepository")
    @patch("api.dashboard.ChallengeRepository")
    @patch("api.dashboard.get_profile")
    @patch("services.profile_service.ProfileRepository")
    def test_complete_challenge_success(
        self, mock_repo, mock_prof, mock_chal, mock_badge
    ):
        """

        Args:
          mock_repo: 
          mock_prof: 
          mock_chal: 
          mock_badge: 

        Returns:

        """
        mock_chal.complete_challenge.return_value = {
            "id": "ch-1",
            "eco_points": 10,
            "is_completed": True,
        }
        mock_prof.return_value = {"eco_points": 40}
        mock_badge.get_all.return_value = []
        mock_repo.update_profile.return_value = {}

        resp = client.post("/api/challenges/ch-1/complete")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"

    @patch("api.dashboard.BadgeRepository")
    @patch("api.dashboard.ChallengeRepository")
    @patch("api.dashboard.get_profile")
    @patch("services.profile_service.ProfileRepository")
    def test_complete_challenge_awards_badge_at_50_points(
        self, mock_repo, mock_prof, mock_chal, mock_badge
    ):
        """

        Args:
          mock_repo: 
          mock_prof: 
          mock_chal: 
          mock_badge: 

        Returns:

        """
        mock_chal.complete_challenge.return_value = {
            "id": "ch-1",
            "eco_points": 10,
            "is_completed": True,
        }
        mock_prof.return_value = {"eco_points": 45}
        mock_badge.get_all.return_value = []
        mock_badge.create.return_value = {}
        mock_repo.update_profile.return_value = {}

        resp = client.post("/api/challenges/ch-1/complete")
        assert resp.status_code == 200
        # Badge should have been created (55 >= 50 and no existing Eco Warrior badge)
        mock_badge.create.assert_called_once()

    @patch("api.dashboard.ChallengeRepository")
    def test_complete_challenge_failure(self, mock_chal):
        """

        Args:
          mock_chal: 

        Returns:

        """
        mock_chal.complete_challenge.side_effect = Exception("DB error")
        resp = client.post("/api/challenges/ch-1/complete")
        assert resp.status_code == 400
