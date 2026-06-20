"""
CarbonIQ Emission Factors.

All emission factors are stored as plain Python dictionaries with full source
attribution.  Values are referenced by the carbon-calculator service and other
services that need to convert user activity into CO₂-equivalent emissions.

Sources
-------
- DEFRA (UK Dept for Environment, Food & Rural Affairs) 2023 GHG Conversion Factors
- EPA (US Environmental Protection Agency) GHG Equivalencies Calculator
- CEA (Central Electricity Authority, India) CO₂ Baseline Database 2023
- IPCC (Intergovernmental Panel on Climate Change) AR6 WG3

All factors are expressed in **kg CO₂e** unless otherwise noted.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Transport emission factors  (kg CO₂e per kilometre)
# ---------------------------------------------------------------------------
TRANSPORT_FACTORS: dict[str, float] = {
    # Source: DEFRA 2023 – average medium car, petrol
    "car_petrol": 0.21,
    # Source: DEFRA 2023 – average medium car, diesel
    "car_diesel": 0.27,
    # Source: EPA 2023 – BEV on average US grid (conservative global proxy)
    "car_electric": 0.05,
    # Source: DEFRA 2023 – average motorcycle
    "motorcycle": 0.11,
    # Source: DEFRA 2023 – local bus, average occupancy
    "bus": 0.089,
    # Source: DEFRA 2023 – national rail, average occupancy
    "train": 0.041,
    # Zero-emission modes
    "bicycle": 0.0,
    "walk": 0.0,
}

# ---------------------------------------------------------------------------
# Electricity emission factor  (kg CO₂e per kWh)
# ---------------------------------------------------------------------------
# Source: CEA (Central Electricity Authority, India) 2023 – weighted average
ELECTRICITY_FACTOR_KG_PER_KWH: float = 0.82

# ---------------------------------------------------------------------------
# Air-conditioning power draw  (kWh per hour of operation)
# ---------------------------------------------------------------------------
# Source: BEE (Bureau of Energy Efficiency, India) – typical 1.5-ton split AC
AC_KWH_PER_HOUR: float = 1.5

# ---------------------------------------------------------------------------
# Diet emission factors  (kg CO₂e per day)
# ---------------------------------------------------------------------------
DIET_FACTORS: dict[str, float] = {
    # Source: IPCC AR6 WG3 – high-meat Western diet
    "meat_heavy": 3.3,
    # Source: IPCC AR6 WG3 – mixed omnivore diet
    "average": 2.5,
    # Source: IPCC AR6 WG3 – lacto-ovo-vegetarian
    "vegetarian": 1.7,
    # Source: IPCC AR6 WG3 – plant-based diet
    "vegan": 1.5,
}

# ---------------------------------------------------------------------------
# Flight emission factors  (kg CO₂e per single flight, one-way)
# ---------------------------------------------------------------------------
FLIGHT_FACTORS: dict[str, float] = {
    # Source: DEFRA 2023 – economy class, domestic / short-haul (< 3 700 km)
    "short_haul": 255.0,
    # Source: DEFRA 2023 – economy class, long-haul (> 3 700 km)
    "long_haul": 1100.0,
}

# ---------------------------------------------------------------------------
# Impact equivalents  (per 1 kg CO₂e)
# Used to translate emissions into relatable everyday comparisons.
# ---------------------------------------------------------------------------
IMPACT_EQUIVALENTS: dict[str, float] = {
    # Source: EPA 2023 – km driven in an average passenger car per kg CO₂
    "driving_km_per_kg": 4.7,
    # Source: EPA 2023 – smartphone full charges per kg CO₂
    "smartphone_charges_per_kg": 100.0,
    # Source: EPA 2023 – kg CO₂ absorbed per mature tree per year
    "trees_per_year_kg": 22.0,
    # Source: DEFRA 2023 – hours of a 10 W LED bulb per kg CO₂
    "led_hours_per_kg": 100.0,
}

# ---------------------------------------------------------------------------
# Cost-saving reference prices  (Indian Rupees)
# Used by the savings-calculator to estimate monetary benefits.
# ---------------------------------------------------------------------------
COST_SAVINGS: dict[str, float] = {
    # Average petrol/diesel fuel cost per km driven (INR) – India 2024
    "fuel_per_km_inr": 5.0,
    # Average domestic electricity tariff (INR per kWh) – India 2024
    "electricity_per_kwh_inr": 8.0,
    # Average public-transport fare per km (INR) – metro/bus blended
    "public_transport_per_km_inr": 2.0,
}

# ---------------------------------------------------------------------------
# Allowed enum values  (used for validation across the application)
# ---------------------------------------------------------------------------
ALLOWED_TRANSPORT_TYPES: list[str] = list(TRANSPORT_FACTORS.keys())
ALLOWED_DIET_TYPES: list[str] = list(DIET_FACTORS.keys())
