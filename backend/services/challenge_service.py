"""
CarbonIQ Challenge Service.

Generates weekly sustainability challenges and manages badge awards.
Challenges are drawn from a curated pool and personalised based on the
user's profile and footprint data.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta
from typing import Any

from models.challenge import Badge, Challenge

logger = logging.getLogger("carboniq.challenges")

# ---------------------------------------------------------------------------
# Challenge pool (15+ challenges across categories)
# ---------------------------------------------------------------------------

_CHALLENGE_POOL: list[dict[str, Any]] = [
    # Transport challenges
    {
        "title": "Walk 2 km Today",
        "description": "Replace a short car trip with a walk. Track your steps!",
        "eco_points": 10,
        "category": "transport",
        "transport_types": ["car_petrol", "car_diesel", "motorcycle"],
    },
    {
        "title": "Take Public Transport",
        "description": "Use bus or metro for your commute today instead of driving.",
        "eco_points": 15,
        "category": "transport",
        "transport_types": ["car_petrol", "car_diesel", "motorcycle"],
    },
    {
        "title": "Cycle to Work",
        "description": "Bike to work or the nearest transit stop. Zero emissions!",
        "eco_points": 20,
        "category": "transport",
        "transport_types": ["car_petrol", "car_diesel", "car_electric", "motorcycle"],
    },
    {
        "title": "Carpool This Week",
        "description": "Find a colleague or neighbour to share rides with for 3 days.",
        "eco_points": 15,
        "category": "transport",
        "transport_types": ["car_petrol", "car_diesel"],
    },
    {
        "title": "No-Drive Day",
        "description": "Go one full day without using a personal vehicle.",
        "eco_points": 10,
        "category": "transport",
        "transport_types": ["car_petrol", "car_diesel", "motorcycle"],
    },
    # Energy challenges
    {
        "title": "Unplug Standby Devices",
        "description": "Unplug 5 devices on standby mode for the entire day.",
        "eco_points": 10,
        "category": "energy",
        "transport_types": [],
    },
    {
        "title": "AC-Free Evening",
        "description": "Skip the AC after 8 PM and use natural ventilation instead.",
        "eco_points": 15,
        "category": "energy",
        "transport_types": [],
    },
    {
        "title": "Cold Water Wash",
        "description": "Wash your clothes in cold water instead of hot – saves 80% of the energy.",
        "eco_points": 10,
        "category": "energy",
        "transport_types": [],
    },
    {
        "title": "Lights-Off Hour",
        "description": "Turn off all unnecessary lights for one hour during the evening.",
        "eco_points": 10,
        "category": "energy",
        "transport_types": [],
    },
    # Food challenges
    {
        "title": "Meatless Monday",
        "description": "Eat only plant-based meals for an entire day.",
        "eco_points": 15,
        "category": "food",
        "transport_types": [],
    },
    {
        "title": "Cook with Local Produce",
        "description": "Prepare a meal using only locally sourced ingredients.",
        "eco_points": 10,
        "category": "food",
        "transport_types": [],
    },
    {
        "title": "Zero Food Waste Day",
        "description": "Plan your meals and use all leftovers – throw nothing edible away.",
        "eco_points": 15,
        "category": "food",
        "transport_types": [],
    },
    {
        "title": "Pack a Home Lunch",
        "description": "Bring homemade food instead of ordering delivery for 3 days.",
        "eco_points": 10,
        "category": "food",
        "transport_types": [],
    },
    # Waste / general challenges
    {
        "title": "Carry a Reusable Bottle",
        "description": "Use your own water bottle all week – no single-use plastic.",
        "eco_points": 10,
        "category": "waste",
        "transport_types": [],
    },
    {
        "title": "Digital Detox Hour",
        "description": "Switch off all screens for one hour to save energy and recharge yourself.",
        "eco_points": 10,
        "category": "waste",
        "transport_types": [],
    },
    {
        "title": "Plant a Sapling",
        "description": "Plant a tree or herb – even a kitchen-garden pot counts!",
        "eco_points": 25,
        "category": "waste",
        "transport_types": [],
    },
]


# ---------------------------------------------------------------------------
# Badge definitions
# ---------------------------------------------------------------------------

_BADGE_DEFINITIONS: list[dict[str, str]] = [
    {
        "badge_name": "First Step",
        "badge_description": "Completed your first carbon footprint calculation.",
        "condition": "first_calculation",
    },
    {
        "badge_name": "Eco Warrior",
        "badge_description": "Completed 5 sustainability challenges.",
        "condition": "5_challenges",
    },
    {
        "badge_name": "Green Hero",
        "badge_description": "Achieved a carbon score below 30 – outstanding!",
        "condition": "score_below_30",
    },
    {
        "badge_name": "Consistency King",
        "badge_description": "Tracked your footprint for 4 consecutive weeks.",
        "condition": "4_weeks",
    },
    {
        "badge_name": "Diet Champion",
        "badge_description": "Switched to a vegetarian or vegan diet.",
        "condition": "diet_switch",
    },
    {
        "badge_name": "Zero Waste Hero",
        "badge_description": "Completed 3 waste-reduction challenges.",
        "condition": "3_waste_challenges",
    },
]


def _get_week_start() -> str:
    """Return the ISO date string for the start (Monday) of the current week."""
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def generate_weekly_challenges(
    profile: dict[str, Any],
    footprint: float | None = None,
) -> list[Challenge]:
    """Select 3 personalised challenges for the current week.

    Selection logic:
        1. If the user drives (car/motorcycle), prioritise transport challenges.
        2. If the user has a meat-heavy diet, prioritise food challenges.
        3. Fill remaining slots from energy and general challenges.

    Args:
        profile: User profile dict (must contain ``transport_type``, ``diet_type``).
        footprint: Optional current monthly footprint for scoring priority.

    Returns:
        A list of 3 ``Challenge`` objects for the current week.
    """
    transport_type = profile.get("transport_type", "").lower()
    diet_type = profile.get("diet_type", "").lower()
    week_start = _get_week_start()

    selected: list[Challenge] = []
    used_titles: set[str] = set()

    # Priority 1: Transport challenges for car/motorcycle users
    if transport_type in ("car_petrol", "car_diesel", "motorcycle"):
        for ch in _CHALLENGE_POOL:
            if (
                ch["category"] == "transport"
                and transport_type in ch.get("transport_types", [])
                and ch["title"] not in used_titles
            ):
                selected.append(_to_challenge(ch, week_start))
                used_titles.add(ch["title"])
                break

    # Priority 2: Food challenges for meat-heavy diet
    if diet_type == "meat_heavy" and len(selected) < 3:
        for ch in _CHALLENGE_POOL:
            if ch["category"] == "food" and ch["title"] not in used_titles:
                selected.append(_to_challenge(ch, week_start))
                used_titles.add(ch["title"])
                break

    # Fill remaining from energy and general categories
    for category in ("energy", "waste", "food", "transport"):
        if len(selected) >= 3:
            break
        for ch in _CHALLENGE_POOL:
            if (
                ch["category"] == category
                and ch["title"] not in used_titles
            ):
                selected.append(_to_challenge(ch, week_start))
                used_titles.add(ch["title"])
                break

    return selected[:3]


def _to_challenge(pool_entry: dict[str, Any], week_start: str) -> Challenge:
    """Convert a pool entry dict into a ``Challenge`` model instance."""
    return Challenge(
        id=str(uuid.uuid4()),
        title=pool_entry["title"],
        description=pool_entry["description"],
        eco_points=pool_entry.get("eco_points", 10),
        is_completed=False,
        week_start=week_start,
    )


def check_badge_eligibility(
    completed_challenges: int,
    carbon_score: int | None = None,
    total_calculations: int = 0,
    diet_type: str = "",
    consecutive_weeks: int = 0,
    waste_challenges: int = 0,
) -> list[Badge]:
    """Check which badges the user is newly eligible for.

    Args:
        completed_challenges: Total completed challenges.
        carbon_score: Latest carbon score (0–100).
        total_calculations: Number of carbon calculations performed.
        diet_type: Current diet type.
        consecutive_weeks: Consecutive weeks of tracking.
        waste_challenges: Completed waste-category challenges.

    Returns:
        A list of ``Badge`` objects the user has just earned.
    """
    earned: list[Badge] = []
    now = datetime.utcnow().isoformat()

    for badge_def in _BADGE_DEFINITIONS:
        condition = badge_def["condition"]

        if condition == "first_calculation" and total_calculations >= 1:
            earned.append(_to_badge(badge_def, now))
        elif condition == "5_challenges" and completed_challenges >= 5:
            earned.append(_to_badge(badge_def, now))
        elif condition == "score_below_30" and carbon_score is not None and carbon_score < 30:
            earned.append(_to_badge(badge_def, now))
        elif condition == "4_weeks" and consecutive_weeks >= 4:
            earned.append(_to_badge(badge_def, now))
        elif condition == "diet_switch" and diet_type in ("vegetarian", "vegan"):
            earned.append(_to_badge(badge_def, now))
        elif condition == "3_waste_challenges" and waste_challenges >= 3:
            earned.append(_to_badge(badge_def, now))

    return earned


def _to_badge(badge_def: dict[str, str], earned_at: str) -> Badge:
    """Convert a badge definition dict into a ``Badge`` model instance."""
    return Badge(
        id=str(uuid.uuid4()),
        badge_name=badge_def["badge_name"],
        badge_description=badge_def["badge_description"],
        earned_at=earned_at,
    )
