"""Tests for CarbonIQ Profile API endpoints."""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=False)


class _FakeUser:
    id = "test-user-uuid"


def _override_auth():
    return _FakeUser()


@pytest.fixture(autouse=True)
def _patch_auth():
    from api.profile import get_current_user
    app.dependency_overrides[get_current_user] = _override_auth
    yield
    app.dependency_overrides.clear()


class TestSignup:
    @patch("api.profile.get_supabase")
    def test_successful_signup(self, mock_sb):
        class MockUser:
            id = "new-user-id"
            email = "new@test.com"
            model_dump = lambda self: {"id": self.id, "email": self.email}

        class MockResponse:
            user = MockUser()

        mock_sb.return_value.auth.sign_up.return_value = MockResponse()
        resp = client.post("/api/auth/signup", json={
            "email": "new@test.com",
            "password": "TestPass123!",
            "name": "New User"
        })
        assert resp.status_code == 200
        assert "message" in resp.json()

    @patch("api.profile.get_supabase")
    def test_signup_failure(self, mock_sb):
        mock_sb.return_value.auth.sign_up.side_effect = Exception("User already exists")
        resp = client.post("/api/auth/signup", json={
            "email": "dup@test.com",
            "password": "TestPass123!",
            "name": "Dup User"
        })
        assert resp.status_code == 400


class TestLogin:
    @patch("api.profile.get_profile")
    @patch("api.profile.get_supabase")
    def test_login_with_complete_profile(self, mock_sb, mock_prof):
        class MockUser:
            id = "user-id"

        class MockSession:
            access_token = "tok"
            model_dump = lambda self: {"access_token": self.access_token}

        class MockResponse:
            user = MockUser()
            session = MockSession()

        mock_sb.return_value.auth.sign_in_with_password.return_value = MockResponse()
        mock_prof.return_value = {"city": "Mumbai"}
        resp = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "password"
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["profile_complete"] is True


class TestGetProfile:
    @patch("api.profile.get_profile")
    def test_get_existing_profile(self, mock_prof):
        mock_prof.return_value = {
            "id": "test-user-uuid",
            "name": "Test",
            "email": "t@t.com",
            "city": "Delhi",
            "transport_type": "bus",
            "diet_type": "average",
            "household_size": 2,
            "eco_points": 50,
        }
        resp = client.get("/api/profile")
        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "Test"

    @patch("api.profile.get_profile")
    def test_get_missing_profile_returns_404(self, mock_prof):
        mock_prof.return_value = None
        resp = client.get("/api/profile")
        assert resp.status_code == 404


class TestUpdateProfile:
    @patch("api.profile.update_profile")
    @patch("api.profile.create_profile")
    @patch("api.profile.get_profile")
    def test_update_existing_profile(self, mock_get, mock_create, mock_update):
        mock_get.return_value = {"id": "test-user-uuid", "name": "Old"}
        mock_update.return_value = {
            "id": "test-user-uuid",
            "name": "Updated",
            "email": "t@t.com",
            "city": "Mumbai",
            "transport_type": "car_petrol",
            "diet_type": "average",
            "household_size": 1,
            "eco_points": 0,
        }
        resp = client.put("/api/profile", json={
            "name": "Updated",
            "email": "t@t.com",
            "city": "Mumbai",
            "transport_type": "car_petrol",
            "diet_type": "average",
            "avg_travel_distance": 15.0,
            "household_size": 2,
        })
        assert resp.status_code == 200

    @patch("api.profile.update_profile")
    @patch("api.profile.create_profile")
    @patch("api.profile.get_profile")
    def test_create_new_profile_if_none_exists(self, mock_get, mock_create, mock_update):
        mock_get.return_value = None
        mock_create.return_value = {
            "id": "test-user-uuid",
            "name": "New",
            "email": "n@t.com",
            "city": "Bangalore",
            "transport_type": "bicycle",
            "diet_type": "vegetarian",
            "household_size": 1,
            "eco_points": 0,
        }
        resp = client.put("/api/profile", json={
            "name": "New",
            "email": "n@t.com",
            "city": "Bangalore",
            "transport_type": "bicycle",
            "diet_type": "vegetarian",
            "avg_travel_distance": 5.0,
            "household_size": 1,
        })
        assert resp.status_code == 200

    @patch("api.profile.update_profile")
    @patch("api.profile.create_profile")
    @patch("api.profile.get_profile")
    def test_update_failure_returns_400(self, mock_get, mock_create, mock_update):
        mock_get.return_value = {"id": "test-user-uuid"}
        mock_update.side_effect = Exception("DB error")
        resp = client.put("/api/profile", json={
            "name": "X",
            "email": "x@t.com",
            "city": "Delhi",
            "transport_type": "bus",
            "diet_type": "average",
            "avg_travel_distance": 10.0,
            "household_size": 1,
        })
        assert resp.status_code == 400
