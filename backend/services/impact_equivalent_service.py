"""
CarbonIQ Impact Equivalent Service.

Translates raw kg CO₂e into relatable everyday equivalents so users can
understand the real-world significance of their footprint.
"""

from __future__ import annotations

from utils.emission_factors import IMPACT_EQUIVALENTS


def calculate_equivalents(kg_co2: float) -> dict[str, float]:
    """Convert kilograms of CO₂e into relatable impact equivalents.
    
    Equivalents calculated:
        * **driving_km** – km driven in an average passenger car
        * **smartphone_charges** – full smartphone charges
        * **trees_to_offset** – mature trees needed for one year to offset
        * **led_bulb_hours** – hours a 10 W LED bulb could run

    Args:
      kg_co2: Total CO₂e in kilograms.
      kg_co2: float: 

    Returns:
      : A dict mapping each equivalent name to its computed value,
      rounded to one decimal place.  All values are ≥ 0.

    """
    if kg_co2 < 0:
        kg_co2 = 0.0

    driving_km = round(kg_co2 * IMPACT_EQUIVALENTS["driving_km_per_kg"], 1)

    smartphone_charges = round(
        kg_co2 * IMPACT_EQUIVALENTS["smartphone_charges_per_kg"], 1
    )

    trees_per_year_absorption = IMPACT_EQUIVALENTS["trees_per_year_kg"]
    trees_to_offset = (
        round(kg_co2 / trees_per_year_absorption, 1)
        if trees_per_year_absorption > 0
        else 0.0
    )

    led_bulb_hours = round(kg_co2 * IMPACT_EQUIVALENTS["led_hours_per_kg"], 1)

    return {
        "driving_km": max(0.0, driving_km),
        "smartphone_charges": max(0.0, smartphone_charges),
        "trees_to_offset": max(0.0, trees_to_offset),
        "led_bulb_hours": max(0.0, led_bulb_hours),
    }
