"""Tests for CarbonIQ Error Handlers."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from utils.error_handlers import (
    CarbonIQError,
    NotFoundError,
    AuthenticationError,
    ForbiddenError,
    register_error_handlers,
)


# Create a test app with error handlers registered
_app = FastAPI()
register_error_handlers(_app)


class StrictInput(BaseModel):
    value: int = Field(..., gt=0)


@_app.get("/test-carboniq-error")
async def raise_carboniq_error():
    raise CarbonIQError(message="Test error", status_code=400, detail={"field": "test"})


@_app.get("/test-not-found")
async def raise_not_found():
    raise NotFoundError(resource="Profile")


@_app.get("/test-auth-error")
async def raise_auth_error():
    raise AuthenticationError()


@_app.get("/test-forbidden")
async def raise_forbidden():
    raise ForbiddenError(message="You cannot do this")


@_app.get("/test-value-error")
async def raise_value_error():
    raise ValueError("Bad input value")


@_app.get("/test-generic-error")
async def raise_generic():
    raise RuntimeError("Something went very wrong")


client = TestClient(_app, raise_server_exceptions=False)


class TestCarbonIQErrorHandler:
    def test_returns_correct_status_and_body(self):
        resp = client.get("/test-carboniq-error")
        assert resp.status_code == 400
        body = resp.json()
        assert body["error"] == "Test error"
        assert body["detail"] == {"field": "test"}


class TestNotFoundErrorHandler:
    def test_returns_404(self):
        resp = client.get("/test-not-found")
        assert resp.status_code == 404
        body = resp.json()
        assert "Profile" in body["error"]


class TestAuthenticationErrorHandler:
    def test_returns_401(self):
        resp = client.get("/test-auth-error")
        assert resp.status_code == 401
        body = resp.json()
        assert body["error"] == "Authentication failed."


class TestForbiddenErrorHandler:
    def test_returns_403(self):
        resp = client.get("/test-forbidden")
        assert resp.status_code == 403
        body = resp.json()
        assert body["error"] == "You cannot do this"


class TestValueErrorHandler:
    def test_returns_400(self):
        resp = client.get("/test-value-error")
        assert resp.status_code == 400
        body = resp.json()
        assert body["error"] == "Bad input value"


class TestGenericErrorHandler:
    def test_returns_500_with_safe_message(self):
        resp = client.get("/test-generic-error")
        assert resp.status_code == 500
        body = resp.json()
        # Should NOT leak internal details
        assert "Something went very wrong" not in body["error"]
        assert "internal server error" in body["error"].lower()


class TestExceptionHierarchy:
    def test_not_found_is_carboniq_error(self):
        assert issubclass(NotFoundError, CarbonIQError)

    def test_auth_error_is_carboniq_error(self):
        assert issubclass(AuthenticationError, CarbonIQError)

    def test_forbidden_is_carboniq_error(self):
        assert issubclass(ForbiddenError, CarbonIQError)

    def test_carboniq_error_defaults(self):
        err = CarbonIQError()
        assert err.status_code == 400
        assert err.message == "An application error occurred."
        assert err.detail == {}

    def test_carboniq_error_custom(self):
        err = CarbonIQError(
            message="Custom", status_code=422, detail={"x": 1}
        )
        assert err.status_code == 422
        assert err.message == "Custom"
        assert err.detail == {"x": 1}
