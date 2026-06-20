"""
CarbonIQ Savings Calculator Service.

Estimates both CO₂ and monetary savings for specific sustainability actions.
Uses emission factors and cost data from ``utils.emission_factors``.
"""

from __future__ import annotations

from typing import Any

from utils.emission_factors import (
    COST_SAVINGS,
    DIET_FACTORS,
    ELECTRICITY_FACTOR_KG_PER_KWH,
    TRANSPORT_FACTORS,
)


# ---------------------------------------------------------------------------
# Lookup table: action → estimated savings
# Each entry has:
#   co2_savings_kg   – estimated monthly CO₂ savings (kg)
#   cost_savings_inr – estimated monthly cost savings (₹)
#   description      – human-readable explanation
# ---------------------------------------------------------------------------

_ACTION_SAVINGS: dict[str, dict[str, Any]] = {
    "switch_to_public_transport": {
        "co2_savings_kg": round(
            (TRANSPORT_FACTORS["car_petrol"] - TRANSPORT_FACTORS["bus"])
            * 15  # avg 15 km/day
            * 30,
            2,
        ),
        "cost_savings_inr": round(
            (COST_SAVINGS["fuel_per_km_inr"] - COST_SAVINGS["public_transport_per_km_inr"])
            * 15
            * 30,
            2,
        ),
        "description": "Switch daily commute from car to bus/metro.",
    },
    "reduce_ac": {
        "co2_savings_kg": round(
            2  # reduce by 2 hours/day
            * 1.5  # AC kWh/hour
            * ELECTRICITY_FACTOR_KG_PER_KWH
            * 30,
            2,
        ),
        "cost_savings_inr": round(
            2 * 1.5 * COST_SAVINGS["electricity_per_kwh_inr"] * 30,
            2,
        ),
        "description": "Reduce AC usage by 2 hours daily.",
    },
    "switch_to_led": {
        "co2_savings_kg": round(
            0.05  # ~50 W savings across house per hour
            * 8  # hours/day
            * ELECTRICITY_FACTOR_KG_PER_KWH
            * 30,
            2,
        ),
        "cost_savings_inr": round(
            0.05 * 8 * COST_SAVINGS["electricity_per_kwh_inr"] * 30,
            2,
        ),
        "description": "Replace all incandescent bulbs with LEDs.",
    },
    "vegetarian_diet": {
        "co2_savings_kg": round(
            (DIET_FACTORS["meat_heavy"] - DIET_FACTORS["vegetarian"]) * 30,
            2,
        ),
        "cost_savings_inr": round(
            15 * 30,  # ~₹15/day saved on meat
            2,
        ),
        "description": "Switch from a meat-heavy diet to vegetarian.",
    },
    "carpool": {
        "co2_savings_kg": round(
            TRANSPORT_FACTORS["car_petrol"] * 15 * 30 * 0.5,
            2,
        ),
        "cost_savings_inr": round(
            COST_SAVINGS["fuel_per_km_inr"] * 15 * 30 * 0.5,
            2,
        ),
        "description": "Carpool with one colleague (halve fuel use).",
    },
    "reduce_flights": {
        "co2_savings_kg": round(255 / 12, 2),  # 1 fewer short-haul flight/year
        "cost_savings_inr": 0.0,  # varies too much to estimate
        "description": "Take one fewer short-haul flight per year.",
    },
    "energy_efficient_appliances": {
        "co2_savings_kg": round(
            50  # ~50 kWh/month saved
            * ELECTRICITY_FACTOR_KG_PER_KWH,
            2,
        ),
        "cost_savings_inr": round(
            50 * COST_SAVINGS["electricity_per_kwh_inr"],
            2,
        ),
        "description": "Upgrade to energy-efficient (5-star) appliances.",
    },
}


def get_action_savings() -> dict[str, dict[str, Any]]:
    """Return the full action-savings lookup table.

    Returns:
        Dict mapping action keys to their savings metadata.
    """
    return _ACTION_SAVINGS.copy()


def calculate_savings(
    recommendations: list[Any],
    current_footprint: float,
    profile: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Estimate per-recommendation savings based on action lookup.

    For each recommendation, the function tries to match its title/description
    to a known action.  If a match is found, the pre-computed savings are
    used; otherwise a conservative default is applied.

    Args:
        recommendations: List of recommendation dicts or objects.
        current_footprint: Current monthly CO₂e in kg.
        profile: Optional user profile dict for personalisation.

    Returns:
        A list of dicts, one per recommendation, containing:
            ``title``, ``co2_savings_kg``, ``cost_savings_inr``, ``description``.
    """
    results: list[dict[str, Any]] = []

    for rec in recommendations:
        if isinstance(rec, dict):
            raw_title = rec.get("title", "")
            desc = rec.get("description", "Apply this recommendation.")
        else:
            raw_title = getattr(rec, "title", "")
            desc = getattr(rec, "description", "Apply this recommendation.")
            
        title = raw_title.lower()
        matched = False

        for action_key, savings in _ACTION_SAVINGS.items():
            # Fuzzy match: check if any keyword from the action key appears
            keywords = action_key.replace("_", " ").split()
            if any(kw in title for kw in keywords):
                results.append({
                    "title": raw_title or action_key,
                    "co2_savings_kg": max(0.0, savings["co2_savings_kg"]),
                    "cost_savings_inr": max(0.0, savings["cost_savings_inr"]),
                    "description": savings["description"],
                })
                matched = True
                break

        if not matched:
            # Conservative default: 5% of current footprint, ₹200 savings
            default_co2 = round(current_footprint * 0.05, 2) if current_footprint > 0 else 5.0
            results.append({
                "title": raw_title or "General improvement",
                "co2_savings_kg": max(0.0, default_co2),
                "cost_savings_inr": 200.0,
                "description": desc,
            })

    return results
