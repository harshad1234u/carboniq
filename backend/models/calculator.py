"""
CarbonIQ Calculator Models.

Pydantic v2 models for carbon footprint calculation input and output.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from utils.emission_factors import ALLOWED_DIET_TYPES, ALLOWED_TRANSPORT_TYPES


class CarbonInput(BaseModel):
    """User-supplied data for a carbon footprint calculation.

    All numeric fields are validated to be non-negative with reasonable caps.
    """

    vehicle_type: str = Field(
        ..., description="Primary vehicle/transport type."
    )
    daily_travel_km: float = Field(
        default=0.0, ge=0, le=500,
        description="Daily travel distance in km.",
    )
    electricity_kwh: float = Field(
        default=0.0, ge=0, le=5000,
        description="Monthly electricity consumption in kWh.",
    )
    ac_hours: float = Field(
        default=0.0, ge=0, le=24,
        description="Average daily AC usage in hours.",
    )
    diet_type: str = Field(
        ..., description="Dietary pattern.",
    )
    flights_short: int = Field(
        default=0, ge=0, le=100,
        description="Number of short-haul flights per year.",
    )
    flights_long: int = Field(
        default=0, ge=0, le=100,
        description="Number of long-haul flights per year.",
    )

    @field_validator("vehicle_type")
    @classmethod
    def validate_vehicle(cls, v: str) -> str:
        """Vehicle type must be in the allowed transport set."""
        normalised = v.strip().lower()
        if normalised not in ALLOWED_TRANSPORT_TYPES:
            raise ValueError(
                f"Invalid vehicle type: '{v}'. "
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


class CarbonScore(BaseModel):
    """Carbon footprint score with traffic-light rating."""

    score: int = Field(..., ge=0, le=100, description="0–100 carbon score.")
    level: str = Field(..., description="Descriptive level name.")
    color: str = Field(..., description="UI colour code.")


class CarbonResult(BaseModel):
    """Full breakdown of a monthly carbon footprint calculation."""

    transport_emissions: float = Field(
        ..., description="Transport CO₂e (kg/month)."
    )
    electricity_emissions: float = Field(
        ..., description="Electricity CO₂e (kg/month)."
    )
    food_emissions: float = Field(
        ..., description="Diet CO₂e (kg/month)."
    )
    flight_emissions: float = Field(
        ..., description="Flight CO₂e (kg/month, annualised)."
    )
    total_emissions: float = Field(
        ..., description="Total CO₂e (kg/month)."
    )
    carbon_score: CarbonScore = Field(
        ..., description="Traffic-light score."
    )
    impact_equivalents: dict[str, float] = Field(
        default_factory=dict,
        description="Relatable impact equivalents.",
    )
