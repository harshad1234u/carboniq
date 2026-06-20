"""
CarbonIQ Carbon Calculator Service.

Core business logic for computing monthly carbon footprints from user inputs.
All emission factors are sourced from ``utils.emission_factors``.
"""

from __future__ import annotations

from models.calculator import CarbonInput, CarbonResult, CarbonScore
from services.impact_equivalent_service import calculate_equivalents
from utils.emission_factors import (
    AC_KWH_PER_HOUR,
    DIET_FACTORS,
    ELECTRICITY_FACTOR_KG_PER_KWH,
    FLIGHT_FACTORS,
    TRANSPORT_FACTORS,
)


def calculate_emissions(carbon_input: CarbonInput) -> CarbonResult:
    """Calculate a full monthly carbon footprint breakdown.

    Calculation methodology:
        * **Transport** = emission_factor[vehicle_type] × daily_km × 30 days
        * **Electricity** = monthly_kWh × grid_factor
        * **AC** = daily_ac_hours × ac_kWh_rate × grid_factor × 30 days
        * **Food** = daily_diet_factor × 30 days
        * **Flights** = (short_haul_flights × 255 + long_haul_flights × 1100) / 12

    Args:
        carbon_input: Validated ``CarbonInput`` from the user.

    Returns:
        A ``CarbonResult`` with the full breakdown, score, and equivalents.
    """
    # --- Transport ---
    transport_factor = TRANSPORT_FACTORS.get(carbon_input.vehicle_type, 0.0)
    transport_emissions = transport_factor * carbon_input.daily_travel_km * 30

    # --- Electricity ---
    electricity_emissions = (
        carbon_input.electricity_kwh * ELECTRICITY_FACTOR_KG_PER_KWH
    )

    # --- AC (additional electricity from air-conditioning) ---
    ac_emissions = (
        carbon_input.ac_hours
        * AC_KWH_PER_HOUR
        * ELECTRICITY_FACTOR_KG_PER_KWH
        * 30
    )

    # Add AC emissions into the electricity bucket
    electricity_emissions += ac_emissions

    # --- Food ---
    diet_factor = DIET_FACTORS.get(carbon_input.diet_type, 2.5)
    food_emissions = diet_factor * 30

    # --- Flights (annualised → monthly) ---
    flight_emissions = (
        carbon_input.flights_short * FLIGHT_FACTORS["short_haul"]
        + carbon_input.flights_long * FLIGHT_FACTORS["long_haul"]
    ) / 12

    # --- Total ---
    total_emissions = round(
        transport_emissions + electricity_emissions + food_emissions + flight_emissions,
        2,
    )

    # --- Score ---
    score = calculate_carbon_score(total_emissions)

    # --- Impact equivalents ---
    equivalents = calculate_equivalents(total_emissions)

    return CarbonResult(
        transport_emissions=round(transport_emissions, 2),
        electricity_emissions=round(electricity_emissions, 2),
        food_emissions=round(food_emissions, 2),
        flight_emissions=round(flight_emissions, 2),
        total_emissions=total_emissions,
        carbon_score=score,
        impact_equivalents=equivalents,
    )


def calculate_carbon_score(total_monthly_kg: float) -> CarbonScore:
    """Derive a 0–100 carbon score from total monthly emissions.

    The score is a linear mapping where ~333 kg/month maps to 100.

    Scoring bands:
        * **0–30**: Green Hero (emerald)
        * **31–60**: Eco Aware (amber)
        * **61–80**: High Impact (orange)
        * **81–100**: Critical (red)

    Args:
        total_monthly_kg: Total monthly CO₂e in kg.

    Returns:
        A ``CarbonScore`` with the numeric score, level name, and colour.
    """
    raw = (total_monthly_kg / 333) * 100
    score = min(100, max(0, int(raw)))

    if score <= 30:
        level = "Green Hero"
        color = "emerald"
    elif score <= 60:
        level = "Eco Aware"
        color = "amber"
    elif score <= 80:
        level = "High Impact"
        color = "orange"
    else:
        level = "Critical"
        color = "red"

    return CarbonScore(score=score, level=level, color=color)
