"""
CarbonIQ Eco-Twin Service.

Computes a "digital twin" prediction: what the user's footprint would
look like after applying one or more recommendations.
"""

from __future__ import annotations
from typing import Any
from models.ai_coach import Recommendation
from models.eco_twin import EcoTwinResponse
from services.impact_equivalent_service import calculate_equivalents


def calculate_eco_twin(
    current_footprint: float,
    recommendations: list[Recommendation],
) -> EcoTwinResponse:
    """Predict the user's footprint after applying recommendations.

    Args:
      current_footprint: Current monthly CO₂e in kg.
      recommendations: List of recommendations with ``co2_savings_kg``.
      current_footprint: float: 
      recommendations: list[Recommendation]: 

    Returns:
      : An ``EcoTwinResponse`` with current vs predicted comparison.

    """
    if current_footprint < 0:
        current_footprint = 0.0

    # Calculate total savings from all recommendations
    total_savings = sum(rec.co2_savings_kg for rec in recommendations)

    # Predicted footprint can never go below zero
    predicted_footprint = max(0.0, current_footprint - total_savings)
    predicted_footprint = round(predicted_footprint, 2)

    # Reduction percentage
    if current_footprint > 0:
        reduction_percentage = round(
            ((current_footprint - predicted_footprint) / current_footprint) * 100,
            1,
        )
    else:
        reduction_percentage = 0.0

    # Cap at 100%
    reduction_percentage = min(100.0, max(0.0, reduction_percentage))

    # Impact equivalents for both scenarios
    current_equivalents = calculate_equivalents(current_footprint)
    predicted_equivalents = calculate_equivalents(predicted_footprint)

    # Per-recommendation impact breakdown
    recommendation_impacts: list[dict[str, Any]] = []
    for rec in recommendations:
        savings = rec.co2_savings_kg
        if current_footprint > 0:
            pct = round((savings / current_footprint) * 100, 1)
        else:
            pct = 0.0
        recommendation_impacts.append(
            {
                "title": rec.title,
                "co2_saved": round(savings, 2),
                "percentage_of_total": pct,
            }
        )

    return EcoTwinResponse(
        current_footprint=round(current_footprint, 2),
        predicted_footprint=predicted_footprint,
        reduction_percentage=reduction_percentage,
        current_equivalents=current_equivalents,
        predicted_equivalents=predicted_equivalents,
        recommendation_impacts=recommendation_impacts,
    )
