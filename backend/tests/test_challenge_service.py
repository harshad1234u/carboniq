"""Tests for CarbonIQ Challenge Service."""

import pytest
from services.challenge_service import (
    generate_weekly_challenges,
    check_badge_eligibility,
    _get_week_start,
    _CHALLENGE_POOL,
)

# ---------------------------------------------------------------------------
# generate_weekly_challenges
# ---------------------------------------------------------------------------


class TestGenerateWeeklyChallenges:
    """Tests for weekly challenge generation."""

    def test_returns_three_challenges(self):
        profile = {"transport_type": "car_petrol", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile)
        assert len(challenges) == 3

    def test_car_user_gets_transport_challenge_first(self):
        profile = {"transport_type": "car_petrol", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile)
        # First challenge should be transport-related for car users
        transport_titles = {
            ch["title"] for ch in _CHALLENGE_POOL if ch["category"] == "transport"
        }
        assert challenges[0].title in transport_titles

    def test_motorcycle_user_gets_transport_challenge(self):
        profile = {"transport_type": "motorcycle", "diet_type": "vegetarian"}
        challenges = generate_weekly_challenges(profile)
        transport_titles = {
            ch["title"] for ch in _CHALLENGE_POOL if ch["category"] == "transport"
        }
        assert challenges[0].title in transport_titles

    def test_meat_heavy_user_gets_food_challenge(self):
        profile = {"transport_type": "bicycle", "diet_type": "meat_heavy"}
        challenges = generate_weekly_challenges(profile)
        food_titles = {
            ch["title"] for ch in _CHALLENGE_POOL if ch["category"] == "food"
        }
        # At least one challenge should be food-related
        food_found = any(c.title in food_titles for c in challenges)
        assert food_found

    def test_bicycle_user_no_transport_priority(self):
        """Bicycle users should not get transport challenges as priority."""
        profile = {"transport_type": "bicycle", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile)
        assert len(challenges) == 3

    def test_electric_car_user(self):
        profile = {"transport_type": "car_electric", "diet_type": "vegan"}
        challenges = generate_weekly_challenges(profile)
        assert len(challenges) == 3

    def test_challenges_have_week_start(self):
        profile = {"transport_type": "bus", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile)
        for ch in challenges:
            assert ch.week_start is not None
            # Should be an ISO date string
            assert len(ch.week_start) == 10  # YYYY-MM-DD

    def test_challenges_not_completed_by_default(self):
        profile = {"transport_type": "bus", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile)
        for ch in challenges:
            assert ch.is_completed is False

    def test_challenges_have_unique_titles(self):
        profile = {"transport_type": "car_petrol", "diet_type": "meat_heavy"}
        challenges = generate_weekly_challenges(profile)
        titles = [c.title for c in challenges]
        assert len(titles) == len(set(titles))

    def test_challenges_have_positive_eco_points(self):
        profile = {"transport_type": "bus", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile)
        for ch in challenges:
            assert ch.eco_points > 0

    def test_empty_profile(self):
        """Should still return 3 challenges even with empty profile."""
        challenges = generate_weekly_challenges({})
        assert len(challenges) == 3

    def test_with_footprint_parameter(self):
        """footprint parameter should not cause errors."""
        profile = {"transport_type": "car_petrol", "diet_type": "average"}
        challenges = generate_weekly_challenges(profile, footprint=500.0)
        assert len(challenges) == 3


# ---------------------------------------------------------------------------
# _get_week_start
# ---------------------------------------------------------------------------


class TestGetWeekStart:
    def test_returns_iso_date_string(self):
        result = _get_week_start()
        assert len(result) == 10
        # Should parse as a date
        from datetime import datetime

        parsed = datetime.fromisoformat(result)
        assert parsed.weekday() == 0  # Monday


# ---------------------------------------------------------------------------
# check_badge_eligibility
# ---------------------------------------------------------------------------


class TestCheckBadgeEligibility:
    def test_first_calculation_badge(self):
        badges = check_badge_eligibility(completed_challenges=0, total_calculations=1)
        names = [b.badge_name for b in badges]
        assert "First Step" in names

    def test_no_badge_zero_calculations(self):
        badges = check_badge_eligibility(completed_challenges=0, total_calculations=0)
        names = [b.badge_name for b in badges]
        assert "First Step" not in names

    def test_eco_warrior_badge_5_challenges(self):
        badges = check_badge_eligibility(completed_challenges=5)
        names = [b.badge_name for b in badges]
        assert "Eco Warrior" in names

    def test_no_eco_warrior_4_challenges(self):
        badges = check_badge_eligibility(completed_challenges=4)
        names = [b.badge_name for b in badges]
        assert "Eco Warrior" not in names

    def test_green_hero_badge_low_score(self):
        badges = check_badge_eligibility(completed_challenges=0, carbon_score=25)
        names = [b.badge_name for b in badges]
        assert "Green Hero" in names

    def test_no_green_hero_high_score(self):
        badges = check_badge_eligibility(completed_challenges=0, carbon_score=50)
        names = [b.badge_name for b in badges]
        assert "Green Hero" not in names

    def test_consistency_king_4_weeks(self):
        badges = check_badge_eligibility(completed_challenges=0, consecutive_weeks=4)
        names = [b.badge_name for b in badges]
        assert "Consistency King" in names

    def test_diet_champion_vegetarian(self):
        badges = check_badge_eligibility(completed_challenges=0, diet_type="vegetarian")
        names = [b.badge_name for b in badges]
        assert "Diet Champion" in names

    def test_diet_champion_vegan(self):
        badges = check_badge_eligibility(completed_challenges=0, diet_type="vegan")
        names = [b.badge_name for b in badges]
        assert "Diet Champion" in names

    def test_no_diet_champion_meat_heavy(self):
        badges = check_badge_eligibility(completed_challenges=0, diet_type="meat_heavy")
        names = [b.badge_name for b in badges]
        assert "Diet Champion" not in names

    def test_zero_waste_hero_3_waste_challenges(self):
        badges = check_badge_eligibility(completed_challenges=3, waste_challenges=3)
        names = [b.badge_name for b in badges]
        assert "Zero Waste Hero" in names

    def test_multiple_badges_at_once(self):
        """User meeting all criteria should earn all badges."""
        badges = check_badge_eligibility(
            completed_challenges=5,
            carbon_score=20,
            total_calculations=10,
            diet_type="vegan",
            consecutive_weeks=4,
            waste_challenges=5,
        )
        names = [b.badge_name for b in badges]
        assert "First Step" in names
        assert "Eco Warrior" in names
        assert "Green Hero" in names
        assert "Consistency King" in names
        assert "Diet Champion" in names
        assert "Zero Waste Hero" in names
        assert len(badges) == 6

    def test_badge_has_earned_at_timestamp(self):
        badges = check_badge_eligibility(completed_challenges=0, total_calculations=1)
        assert len(badges) > 0
        assert badges[0].earned_at is not None
