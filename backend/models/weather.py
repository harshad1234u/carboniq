"""
CarbonIQ Weather Models.

Pydantic v2 model for weather data returned by the weather service.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """Current weather conditions for a city."""

    city: str = Field(..., description="City name.")
    temperature: float = Field(..., description="Temperature in °C.")
    description: str = Field(..., description="Weather description.")
    humidity: int = Field(..., description="Humidity percentage.")
    icon: str = Field(default="01d", description="OpenWeather icon code.")
