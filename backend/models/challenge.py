"""
CarbonIQ Challenge & Badge Models.

Pydantic v2 models for weekly challenges and gamification badges.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Challenge(BaseModel):
    """A weekly sustainability challenge."""

    id: str = Field(default="", description="Challenge UUID.")
    title: str = Field(..., description="Challenge title.")
    description: str = Field(..., description="What the user needs to do.")
    eco_points: int = Field(
        default=10, ge=0, description="Points awarded on completion."
    )
    is_completed: bool = Field(
        default=False, description="Whether the challenge is done."
    )
    week_start: Optional[str] = Field(
        default=None, description="ISO date of the week this challenge belongs to."
    )


class Badge(BaseModel):
    """An earned sustainability badge."""

    id: str = Field(default="", description="Badge UUID.")
    badge_name: str = Field(..., description="Badge name.")
    badge_description: str = Field(
        ..., description="What the badge recognises."
    )
    earned_at: Optional[str] = Field(
        default=None, description="ISO timestamp when earned."
    )
