"""
CarbonIQ Profile & Auth Models.

Pydantic v2 models for user profile CRUD and authentication flows.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from utils.emission_factors import ALLOWED_DIET_TYPES, ALLOWED_TRANSPORT_TYPES

# ---------------------------------------------------------------------------
# Auth models
# ---------------------------------------------------------------------------


class AuthSignup(BaseModel):
    """Payload for user registration."""

    email: str = Field(..., description="User email address.")
    password: str = Field(
        ..., min_length=6, max_length=128, description="Password (min 6 chars)."
    )
    name: str = Field(..., min_length=1, max_length=120, description="Display name.")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Basic email format check."""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v.strip()):
            raise ValueError("Invalid email format.")
        return v.strip().lower()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is non-empty after stripping."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Name must not be empty.")
        return cleaned


class AuthLogin(BaseModel):
    """Payload for user login."""

    email: str = Field(..., description="User email address.")
    password: str = Field(..., description="Password.")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Basic email format check."""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v.strip()):
            raise ValueError("Invalid email format.")
        return v.strip().lower()


# ---------------------------------------------------------------------------
# Profile models
# ---------------------------------------------------------------------------


class ProfileCreate(BaseModel):
    """Payload for creating / updating a user profile."""

    name: str = Field(..., min_length=1, max_length=120, description="Display name.")
    email: Optional[str] = Field(default=None, description="User email address.")
    city: str = Field(
        ..., min_length=1, max_length=100, description="City of residence."
    )
    transport_type: str = Field(..., description="Primary transport mode.")
    avg_travel_distance: float = Field(
        ..., ge=0, le=500, description="Average daily travel distance in km."
    )
    diet_type: str = Field(..., description="Dietary pattern.")
    household_size: int = Field(
        ..., ge=1, le=20, description="Number of household members."
    )

    @field_validator("city")
    @classmethod
    def validate_city(cls, v: str) -> str:
        """City must be a non-empty string."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("City must not be empty.")
        return cleaned

    @field_validator("transport_type")
    @classmethod
    def validate_transport(cls, v: str) -> str:
        """Transport type must be in the allowed set."""
        normalised = v.strip().lower()
        if normalised not in ALLOWED_TRANSPORT_TYPES:
            raise ValueError(
                f"Invalid transport type: '{v}'. "
                f"Allowed: {', '.join(ALLOWED_TRANSPORT_TYPES)}."
            )
        return normalised

    @field_validator("diet_type")
    @classmethod
    def validate_diet(cls, v: str) -> str:
        """Diet type must be in the allowed set."""
        normalised = v.strip().lower()
        if normalised not in ALLOWED_DIET_TYPES:
            raise ValueError(
                f"Invalid diet type: '{v}'. "
                f"Allowed: {', '.join(ALLOWED_DIET_TYPES)}."
            )
        return normalised


class ProfileResponse(BaseModel):
    """Full profile returned to the client."""

    id: str = Field(..., description="User UUID.")
    name: str = Field(default="", description="Display name.")
    email: str = Field(default="", description="Email address.")
    city: str = Field(default="", description="City of residence.")
    transport_type: str = Field(default="", description="Primary transport.")
    avg_travel_distance: float = Field(default=0.0, description="Daily km.")
    diet_type: str = Field(default="", description="Dietary pattern.")
    household_size: int = Field(default=1, description="Household members.")
    eco_points: int = Field(default=0, description="Gamification points.")
    created_at: Optional[str] = Field(default=None, description="ISO timestamp.")
