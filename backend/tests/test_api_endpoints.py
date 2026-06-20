"""Tests for CarbonIQ API endpoints (Carbon, Dashboard, Profile).

All tests mock the auth dependency and database repositories so no live
Supabase connection is required.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Helpers: mock the get_current_user dependency
# ---------------------------------------------------------------------------


class _FakeUser:
    """ """
    id = "test-user-uuid"


def _override_auth():
    """ """
    return _FakeUser()


# Apply the override globally for this module
app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def _patch_auth():
    """ """
    from api.profile import get_current_user

    app.dependency_overrides[get_current_user] = _override_auth
    yield
    app.dependency_overrides.clear()


# ===================================================================
# Carbon API
# ===================================================================


class TestCalculateCarbon:
    """ """
    @patch("api.carbon.CarbonRepository")
    def test_successful_calculation(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.create_entry.return_value = {}
        payload = {
            "vehicle_type": "car_petrol",
            "daily_travel_km": 20,
            "electricity_kwh": 300,
            "ac_hours": 4,
            "diet_type": "average",
            "flights_short": 2,
            "flights_long": 0,
        }
        resp = client.post("/api/carbon/calculate", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert "total_emissions" in body
        assert body["total_emissions"] > 0
        assert "carbon_score" in body

    @patch("api.carbon.CarbonRepository")
    def test_zero_travel_valid(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.create_entry.return_value = {}
        payload = {
            "vehicle_type": "bicycle",
            "daily_travel_km": 0,
            "electricity_kwh": 0,
            "ac_hours": 0,
            "diet_type": "vegan",
            "flights_short": 0,
            "flights_long": 0,
        }
        resp = client.post("/api/carbon/calculate", json=payload)
        assert resp.status_code == 200

    def test_invalid_vehicle_type_rejected(self):
        """ """
        payload = {
            "vehicle_type": "spaceship",
            "daily_travel_km": 10,
            "electricity_kwh": 100,
            "ac_hours": 2,
            "diet_type": "average",
        }
        resp = client.post("/api/carbon/calculate", json=payload)
        assert resp.status_code == 422  # Validation error

    def test_negative_travel_km_rejected(self):
        """ """
        payload = {
            "vehicle_type": "car_petrol",
            "daily_travel_km": -10,
            "electricity_kwh": 100,
            "ac_hours": 2,
            "diet_type": "average",
        }
        resp = client.post("/api/carbon/calculate", json=payload)
        assert resp.status_code == 422

    def test_missing_required_fields(self):
        """ """
        resp = client.post("/api/carbon/calculate", json={})
        assert resp.status_code == 422


class TestWeatherEndpoint:
    """ """
    def test_get_weather_returns_data(self):
        """ """
        resp = client.get("/api/carbon/weather/London")
        assert resp.status_code == 200
        body = resp.json()
        assert "temperature" in body
        assert "city" in body

    def test_get_weather_empty_city(self):
        """ """
        resp = client.get("/api/carbon/weather/ ")
        assert resp.status_code == 200  # Falls back to default weather


class TestAiCoachEndpoint:
    """ """
    @patch("api.carbon.RecommendationRepository")
    @patch("api.carbon.CarbonRepository")
    @patch("api.carbon.get_profile")
    def test_no_profile_returns_error(self, mock_prof, mock_carbon, mock_rec):
        """

        Args:
          mock_prof: 
          mock_carbon: 
          mock_rec: 

        Returns:

        """
        mock_prof.return_value = None
        resp = client.post("/api/carbon/ai-coach")
        assert resp.status_code == 404

    @patch("api.carbon.RecommendationRepository")
    @patch("api.carbon.CarbonRepository")
    @patch("api.carbon.get_profile")
    def test_no_entries_returns_error(self, mock_prof, mock_carbon, mock_rec):
        """

        Args:
          mock_prof: 
          mock_carbon: 
          mock_rec: 

        Returns:

        """
        mock_prof.return_value = {
            "city": "Mumbai",
            "transport_type": "car_petrol",
            "diet_type": "average",
        }
        mock_carbon.get_latest.return_value = None
        resp = client.post("/api/carbon/ai-coach")
        assert resp.status_code == 400


# ===================================================================
# Dashboard API
# ===================================================================


class TestDashboardSummary:
    """ """
    @patch("api.dashboard.BadgeRepository")
    @patch("api.dashboard.ChallengeRepository")
    @patch("api.dashboard.CarbonRepository")
    @patch("api.dashboard.get_profile")
    def test_no_profile_returns_404(
        self, mock_prof, mock_carbon, mock_chal, mock_badge
    ):
        """

        Args:
          mock_prof: 
          mock_carbon: 
          mock_chal: 
          mock_badge: 

        Returns:

        """
        mock_prof.return_value = None
        resp = client.get("/api/dashboard/summary")
        assert resp.status_code == 404

    @patch("api.dashboard.BadgeRepository")
    @patch("api.dashboard.ChallengeRepository")
    @patch("api.dashboard.CarbonRepository")
    @patch("api.dashboard.get_profile")
    def test_dashboard_with_no_entries(
        self, mock_prof, mock_carbon, mock_chal, mock_badge
    ):
        """

        Args:
          mock_prof: 
          mock_carbon: 
          mock_chal: 
          mock_badge: 

        Returns:

        """
        mock_prof.return_value = {
            "city": "Delhi",
            "transport_type": "bus",
            "diet_type": "average",
            "eco_points": 0,
        }
        mock_carbon.get_latest.return_value = None
        mock_carbon.get_history.return_value = []
        mock_chal.get_current.return_value = []
        mock_chal.create_challenges.return_value = None
        mock_badge.get_all.return_value = []
        # After generating challenges, get_current returns some
        mock_chal.get_current.side_effect = [
            [],  # First call: no challenges exist
            [  # Second call: after generation
                {
                    "id": "1",
                    "title": "Test",
                    "description": "Desc",
                    "eco_points": 10,
                    "is_completed": False,
                    "week_start": "2026-06-16",
                },
            ],
        ]
        resp = client.get("/api/dashboard/summary")
        assert resp.status_code == 200
        body = resp.json()
        assert body["latest_score"] == 0
        assert body["monthly_footprint"] == 0


class TestDashboardHistory:
    """ """
    @patch("api.dashboard.CarbonRepository")
    def test_returns_empty_history(self, mock_carbon):
        """

        Args:
          mock_carbon: 

        Returns:

        """
        mock_carbon.get_history.return_value = []
        resp = client.get("/api/dashboard/history")
        assert resp.status_code == 200
        assert resp.json() == []

    @patch("api.dashboard.CarbonRepository")
    def test_returns_history_entries(self, mock_carbon):
        """

        Args:
          mock_carbon: 

        Returns:

        """
        mock_carbon.get_history.return_value = [
            {
                "recorded_date": "2026-06-19",
                "total_emissions": 350,
                "carbon_score": 65,
                "carbon_level": "Eco Aware",
            },
        ]
        resp = client.get("/api/dashboard/history")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["total_emissions"] == 350


class TestChallengesEndpoint:
    """ """
    @patch("api.dashboard.ChallengeRepository")
    def test_returns_challenges(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.get_current.return_value = [
            {
                "id": "1",
                "title": "Walk 2 km",
                "description": "Walk!",
                "eco_points": 10,
                "is_completed": False,
                "week_start": "2026-06-16",
            },
        ]
        resp = client.get("/api/challenges")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1

    @patch("api.dashboard.ChallengeRepository")
    def test_returns_empty_list(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.get_current.return_value = []
        resp = client.get("/api/challenges")
        assert resp.status_code == 200
        assert resp.json() == []


class TestBadgesEndpoint:
    """ """
    @patch("api.dashboard.BadgeRepository")
    def test_returns_badges(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.get_all.return_value = [
            {
                "id": "1",
                "badge_name": "First Step",
                "badge_description": "Completed first calc",
                "earned_at": "2026-06-19",
            },
        ]
        resp = client.get("/api/badges")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["badge_name"] == "First Step"
