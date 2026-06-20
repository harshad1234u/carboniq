"""
CarbonIQ Dashboard Models.

Pydantic v2 models for the user dashboard and history views.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from models.challenge import Badge, Challenge


class HistoryEntry(BaseModel):
    """A single historical carbon-footprint record."""

    recorded_date: str = Field(..., description="ISO date of the entry.")
    total_emissions: float = Field(..., description="Total CO₂e for that period (kg).")
    carbon_score: int = Field(..., ge=0, le=100, description="0–100 score.")
    carbon_level: str = Field(..., description="Level label.")


class DashboardSummary(BaseModel):
    """Aggregated dashboard data for the current user."""

    latest_score: Optional[int] = Field(
        default=None, description="Most recent carbon score."
    )
    monthly_footprint: Optional[float] = Field(
        default=None, description="Latest total monthly emissions (kg)."
    )
    impact_equivalents: dict[str, float] = Field(
        default_factory=dict,
        description="Latest impact equivalents.",
    )
    active_challenges: list[Challenge] = Field(
        default_factory=list,
        description="Current week's challenges.",
    )
    recent_badges: list[Badge] = Field(
        default_factory=list,
        description="Recently earned badges.",
    )
    trend: list[HistoryEntry] = Field(
        default_factory=list,
        description="Recent history for charting.",
    )
    eco_points: int = Field(
        default=0,
        description="Total eco points earned.",
    )
