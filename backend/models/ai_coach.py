"""
CarbonIQ AI Coach Models.

Pydantic v2 models for Gemini-powered personalised recommendations.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from models.weather import WeatherData


class Recommendation(BaseModel):
    """A single actionable sustainability recommendation."""

    title: str = Field(..., description="Short recommendation title.")
    description: str = Field(
        ..., description="Detailed explanation of the recommendation."
    )
    co2_savings_kg: float = Field(
        ..., ge=0, description="Estimated monthly CO₂e savings in kg."
    )
    cost_savings_inr: float = Field(
        ..., ge=0, description="Estimated monthly cost savings in INR."
    )
    difficulty: str = Field(
        default="medium",
        description="Difficulty level: easy, medium, hard.",
    )


class AiCoachResponse(BaseModel):
    """Full AI coach response with recommendations and context."""

    recommendations: list[Recommendation] = Field(
        ..., description="Ordered list of recommendations."
    )
    total_co2_savings: float = Field(
        ..., ge=0, description="Sum of CO₂e savings across all recommendations."
    )
    total_cost_savings: float = Field(
        ..., ge=0, description="Sum of cost savings across all recommendations."
    )
    weather_context: Optional[WeatherData] = Field(
        default=None, description="Weather data used for context, if available."
    )
