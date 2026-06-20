"""
CarbonIQ AI Coach Service.

Generates personalised sustainability recommendations using Google Gemini.
Falls back to a curated rule-based recommendation engine when the AI is
unavailable.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from models.ai_coach import AiCoachResponse, Recommendation
from models.calculator import CarbonResult
from models.weather import WeatherData
from utils.config import settings

logger = logging.getLogger("carboniq.ai_coach")

# ---------------------------------------------------------------------------
# Pre-defined fallback recommendations
# ---------------------------------------------------------------------------

_FALLBACK_RECOMMENDATIONS: dict[str, list[Recommendation]] = {
    "transport": [
        Recommendation(
            title="Switch to Public Transport",
            description="Replace car commutes with bus or metro to cut emissions by up to 75%.",
            co2_savings_kg=54.5,
            cost_savings_inr=1350.0,
            difficulty="medium",
        ),
        Recommendation(
            title="Start Carpooling",
            description="Share rides with colleagues to halve your transport emissions and fuel costs.",
            co2_savings_kg=47.25,
            cost_savings_inr=1125.0,
            difficulty="easy",
        ),
        Recommendation(
            title="Try Cycling for Short Trips",
            description="Use a bicycle for trips under 5 km – zero emissions and great exercise.",
            co2_savings_kg=18.9,
            cost_savings_inr=450.0,
            difficulty="medium",
        ),
    ],
    "electricity": [
        Recommendation(
            title="Reduce AC by 2 Hours Daily",
            description="Set the AC timer and use fans during cooler parts of the day.",
            co2_savings_kg=73.8,
            cost_savings_inr=720.0,
            difficulty="easy",
        ),
        Recommendation(
            title="Switch to LED Lighting",
            description="Replace all incandescent bulbs with LEDs – they use 80% less energy.",
            co2_savings_kg=9.84,
            cost_savings_inr=96.0,
            difficulty="easy",
        ),
        Recommendation(
            title="Upgrade to 5-Star Appliances",
            description="Energy-efficient refrigerators, ACs, and washing machines save 30-50% power.",
            co2_savings_kg=41.0,
            cost_savings_inr=400.0,
            difficulty="hard",
        ),
    ],
    "food": [
        Recommendation(
            title="Try Vegetarian Mondays",
            description="Replace meat with plant-based meals at least once a week.",
            co2_savings_kg=6.86,
            cost_savings_inr=60.0,
            difficulty="easy",
        ),
        Recommendation(
            title="Switch to a Vegetarian Diet",
            description="A vegetarian diet produces roughly half the emissions of a meat-heavy one.",
            co2_savings_kg=48.0,
            cost_savings_inr=450.0,
            difficulty="medium",
        ),
        Recommendation(
            title="Reduce Food Waste",
            description="Plan meals and store food properly to cut waste by 50%.",
            co2_savings_kg=12.5,
            cost_savings_inr=500.0,
            difficulty="easy",
        ),
    ],
    "flights": [
        Recommendation(
            title="Replace One Flight with a Train",
            description="A single short-haul flight emits 255 kg CO₂ – trains emit 6× less.",
            co2_savings_kg=21.25,
            cost_savings_inr=0.0,
            difficulty="medium",
        ),
    ],
}


def _select_fallback_recommendations(
    footprint: CarbonResult,
) -> list[Recommendation]:
    """Select the best fallback recommendations based on the highest category.

    Args:
      footprint: The user's calculated carbon result.
      footprint: CarbonResult: 

    Returns:
      : A list of 3 ``Recommendation`` objects.

    """
    categories = {
        "transport": footprint.transport_emissions,
        "electricity": footprint.electricity_emissions,
        "food": footprint.food_emissions,
        "flights": footprint.flight_emissions,
    }

    # Sort categories by emissions descending
    sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)

    recs: list[Recommendation] = []
    for cat_name, _ in sorted_cats:
        for rec in _FALLBACK_RECOMMENDATIONS.get(cat_name, []):
            if len(recs) >= 3:
                break
            if rec not in recs:
                recs.append(rec)
        if len(recs) >= 3:
            break

    # Fill with transport recs if we still don't have 3
    while len(recs) < 3:
        for rec in _FALLBACK_RECOMMENDATIONS["transport"]:
            if rec not in recs:
                recs.append(rec)
                break
        else:
            break

    return recs[:3]


def _build_prompt(
    footprint: CarbonResult,
    weather: WeatherData | None,
    profile: dict[str, Any],
) -> str:
    """Build a structured prompt for Gemini.

    Args:
      footprint: Carbon result breakdown.
      weather: Current weather context.
      profile: User profile dict.
      footprint: CarbonResult: 
      weather: WeatherData | None: 
      profile: dict[str: 
      Any]: 

    Returns:
      : A prompt string requesting JSON-formatted recommendations.

    """
    weather_info = ""
    if weather:
        weather_info = (
            f"Current weather in {weather.city}: {weather.temperature}°C, "
            f"{weather.description}, humidity {weather.humidity}%."
        )

    return f"""You are CarbonIQ, an AI sustainability coach. Analyse the user's carbon footprint and provide exactly 3 personalised recommendations to reduce emissions.

USER PROFILE:
- City: {profile.get('city', 'Unknown')}
- Transport: {profile.get('transport_type', 'Unknown')}
- Diet: {profile.get('diet_type', 'Unknown')}
- Household size: {profile.get('household_size', 1)}

MONTHLY EMISSIONS BREAKDOWN (kg CO₂e):
- Transport: {footprint.transport_emissions}
- Electricity: {footprint.electricity_emissions}
- Food: {footprint.food_emissions}
- Flights: {footprint.flight_emissions}
- Total: {footprint.total_emissions}
- Carbon Score: {footprint.carbon_score.score}/100 ({footprint.carbon_score.level})

{weather_info}

Respond ONLY with valid JSON in this exact format:
{{
  "recommendations": [
    {{
      "title": "Short action title",
      "description": "Detailed explanation with specific steps",
      "co2_savings_kg": 25.0,
      "cost_savings_inr": 500.0,
      "difficulty": "easy"
    }}
  ]
}}

Rules:
- Focus on the HIGHEST emission category first.
- co2_savings_kg must be realistic monthly savings in kg.
- cost_savings_inr must be in Indian Rupees.
- difficulty must be "easy", "medium", or "hard".
- Consider weather when suggesting outdoor activities.
- Be specific and actionable.
"""


async def get_recommendations(
    footprint: CarbonResult,
    weather: WeatherData | None,
    profile: dict[str, Any],
) -> AiCoachResponse:
    """Get personalised recommendations using Gemini with rule-based fallback.

    Attempts to call the Gemini API with a structured prompt. If the call
    fails (network error, invalid key, quota, malformed response), the
    function transparently falls back to curated recommendations selected
    based on the user's highest emission category.

    Args:
        footprint: The user's calculated carbon result.
        weather: Current weather data (may be ``None``).
        profile: User profile dict.

    Returns:
        An ``AiCoachResponse`` with 3 recommendations and savings totals.
    """
    # Try Gemini first
    api_key = settings.gemini_api_key
    if api_key:
        try:
            recs = await _call_gemini(footprint, weather, profile, api_key)
            if recs:
                total_co2 = round(sum(r.co2_savings_kg for r in recs), 2)
                total_cost = round(sum(r.cost_savings_inr for r in recs), 2)
                return AiCoachResponse(
                    recommendations=recs,
                    total_co2_savings=total_co2,
                    total_cost_savings=total_cost,
                    weather_context=weather,
                )
        except Exception as exc:
            logger.warning("Gemini call failed, using fallback: %s", exc)

    # Fallback to rule-based recommendations
    logger.info("Using fallback recommendations.")
    recs = _select_fallback_recommendations(footprint)
    total_co2 = round(sum(r.co2_savings_kg for r in recs), 2)
    total_cost = round(sum(r.cost_savings_inr for r in recs), 2)

    return AiCoachResponse(
        recommendations=recs,
        total_co2_savings=total_co2,
        total_cost_savings=total_cost,
        weather_context=weather,
    )


async def _call_gemini(
    footprint: CarbonResult,
    weather: WeatherData | None,
    profile: dict[str, Any],
    api_key: str,
) -> list[Recommendation] | None:
    """Call Google Gemini and parse the response.

    Args:
        footprint: Carbon result.
        weather: Weather data.
        profile: User profile.
        api_key: Gemini API key.

    Returns:
        A list of ``Recommendation`` objects, or ``None`` on failure.
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = _build_prompt(footprint, weather, profile)
        response = model.generate_content(prompt)

        if not response or not response.text:
            logger.warning("Empty Gemini response.")
            return None

        # Extract JSON from the response
        text = response.text.strip()

        # Handle markdown-wrapped JSON
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1]) if len(lines) > 2 else text

        data = json.loads(text)
        raw_recs = data.get("recommendations", [])

        recs: list[Recommendation] = []
        for raw in raw_recs[:3]:
            recs.append(
                Recommendation(
                    title=str(raw.get("title", "Recommendation")),
                    description=str(raw.get("description", "")),
                    co2_savings_kg=max(0, float(raw.get("co2_savings_kg", 10))),
                    cost_savings_inr=max(0, float(raw.get("cost_savings_inr", 0))),
                    difficulty=str(raw.get("difficulty", "medium")),
                )
            )

        return recs if recs else None

    except json.JSONDecodeError as exc:
        logger.warning("Failed to parse Gemini JSON: %s", exc)
        return None
    except ImportError:
        logger.warning("google-generativeai not installed.")
        return None
    except Exception as exc:
        logger.warning("Gemini error: %s", exc)
        return None
