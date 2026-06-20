import pytest
from fastapi.testclient import TestClient
from main import app
from models.profile import AuthSignup, AuthLogin

client = TestClient(app)

def test_missing_profile_after_auth(mocker):
    # Mock supabase client
    class MockUser:
        id = "123"
    
    class MockAuthResponse:
        user = MockUser()
        session = {"access_token": "fake_token"}

    class MockAuth:
        def sign_in_with_password(self, creds):
            return MockAuthResponse()
            
    class MockSupabase:
        auth = MockAuth()
        
    mocker.patch("api.profile.get_supabase", return_value=MockSupabase())
    
    # Mock get_profile to return None (missing profile)
    mocker.patch("api.profile.get_profile", return_value=None)
    
    response = client.post("/api/auth/login", json={"email": "test@test.com", "password": "pwd"})
    assert response.status_code == 200
    data = response.json()
    assert data["profile_complete"] is False

def test_invalid_auth_credentials(mocker):
    # Simulate invalid login
    class MockAuth:
        def sign_in_with_password(self, creds):
            raise Exception("Invalid login credentials")
            
    class MockSupabase:
        auth = MockAuth()
        
    mocker.patch("api.profile.get_supabase", return_value=MockSupabase())
    
    response = client.post("/api/auth/login", json={"email": "wrong@test.com", "password": "bad"})
    assert response.status_code == 401

def test_expired_session(mocker):
    # Mock supabase client so auth.get_user raises, simulating expired JWT
    class MockAuth:
        def get_user(self, token):
            raise Exception("Token expired")

    class MockSupabase:
        auth = MockAuth()

    mocker.patch("api.profile.get_supabase", return_value=MockSupabase())

    response = client.get("/api/profile", headers={"Authorization": "Bearer expired_token"})
    # get_current_user catches the exception and returns 401
    assert response.status_code == 401

