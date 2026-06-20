"""
CarbonIQ Eco-Twin Models.

Pydantic v2 models for the "digital twin" before/after prediction feature.
"""

from __future__ import annotations

from typing import Optional, Any

from pydantic import BaseModel, Field


class EcoTwinRequest(BaseModel):
    """Client request to compute an eco-twin prediction."""

    entry_id: str = Field(
        ..., description="ID of the carbon entry to base predictions on."
    )
    recommendation_id: Optional[str] = Field(
        default=None,
        description="Specific recommendation set ID (uses latest if None).",
    )


class EcoTwinResponse(BaseModel):
    """Predicted footprint comparison after applying recommendations."""

    current_footprint: float = Field(..., description="Current monthly CO₂e in kg.")
    predicted_footprint: float = Field(
        ..., description="Predicted monthly CO₂e after improvements."
    )
    reduction_percentage: float = Field(
        ..., description="Percentage reduction achieved."
    )
    current_equivalents: dict[str, float] = Field(
        default_factory=dict,
        description="Impact equivalents for current footprint.",
    )
    predicted_equivalents: dict[str, float] = Field(
        default_factory=dict,
        description="Impact equivalents for predicted footprint.",
    )
    recommendation_impacts: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Per-recommendation impact breakdown.",
    )
