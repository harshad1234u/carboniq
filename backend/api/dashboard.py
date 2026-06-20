import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from api.profile import get_current_user
from models.dashboard import DashboardSummary, HistoryEntry
from models.challenge import Challenge, Badge
from services.profile_service import get_profile
from services.challenge_service import generate_weekly_challenges
from services.impact_equivalent_service import calculate_equivalents
from database.repositories import CarbonRepository, ChallengeRepository, BadgeRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


@router.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary(user=Depends(get_current_user)) -> DashboardSummary:
    try:
        profile = get_profile(user.id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        latest_entry = CarbonRepository.get_latest(user.id)

        # Challenges
        challenges = ChallengeRepository.get_current(user.id)
        if not challenges:
            # Generate new ones
            footprint = latest_entry["total_emissions"] if latest_entry else None
            generated = generate_weekly_challenges(profile, footprint)
            challenges_data = []
            for c in generated:
                c_dict = c.model_dump(exclude={"id"})
                c_dict["profile_id"] = user.id
                challenges_data.append(c_dict)
            ChallengeRepository.create_challenges(challenges_data)
            challenges = ChallengeRepository.get_current(user.id)

        active_challenges = [
            Challenge(**c) for c in challenges if not c.get("is_completed")
        ]

        # Badges
        badges_data = BadgeRepository.get_all(user.id)
        recent_badges = [Badge(**b) for b in badges_data[:3]]

        # Trend
        history_data = CarbonRepository.get_history(user.id, limit=5)
        trend = [
            HistoryEntry(
                recorded_date=h["recorded_date"],
                total_emissions=h["total_emissions"],
                carbon_score=h["carbon_score"],
                carbon_level=h["carbon_level"],
            )
            for h in history_data
        ]
        trend.reverse()  # chronological order for charts

        if latest_entry:
            return DashboardSummary(
                latest_score=latest_entry["carbon_score"],
                monthly_footprint=latest_entry["total_emissions"],
                impact_equivalents=calculate_equivalents(
                    latest_entry["total_emissions"]
                ),
                active_challenges=active_challenges,
                recent_badges=recent_badges,
                trend=trend,
                eco_points=profile.get("eco_points", 0),
            )
        else:
            return DashboardSummary(
                latest_score=0,
                monthly_footprint=0,
                impact_equivalents=calculate_equivalents(0),
                active_challenges=active_challenges,
                recent_badges=recent_badges,
                trend=[],
                eco_points=profile.get("eco_points", 0),
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dashboard summary error: {e}")
        raise HTTPException(status_code=500, detail="Failed to load dashboard summary")


@router.get("/dashboard/history", response_model=List[HistoryEntry])
async def get_history(user=Depends(get_current_user)) -> List[HistoryEntry]:
    history_data = CarbonRepository.get_history(user.id, limit=20)
    return [
        HistoryEntry(
            recorded_date=h["recorded_date"],
            total_emissions=h["total_emissions"],
            carbon_score=h["carbon_score"],
            carbon_level=h["carbon_level"],
        )
        for h in history_data
    ]


@router.get("/challenges", response_model=List[Challenge])
async def get_challenges(user=Depends(get_current_user)) -> List[Challenge]:
    challenges = ChallengeRepository.get_current(user.id)
    return [Challenge(**c) for c in challenges]


@router.post("/challenges/{id}/complete")
async def complete_challenge(id: str, user=Depends(get_current_user)) -> dict:
    try:
        updated = ChallengeRepository.complete_challenge(id, user.id)

        # Award points
        profile = get_profile(user.id)
        if profile and updated:
            new_points = profile.get("eco_points", 0) + updated.get("eco_points", 0)
            from services.profile_service import update_profile

            update_profile(user.id, {"eco_points": new_points})

            # Simple logic to award badge if reaching 50 points
            if new_points >= 50 and not any(
                b["badge_name"] == "Eco Warrior"
                for b in BadgeRepository.get_all(user.id)
            ):
                BadgeRepository.create(
                    {
                        "profile_id": user.id,
                        "badge_name": "Eco Warrior",
                        "badge_description": "Earned 50 eco points from challenges!",
                    }
                )

        return {"status": "success", "challenge": updated}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Complete challenge error: {e}")
        raise HTTPException(status_code=400, detail="Failed to complete challenge")


@router.get("/badges", response_model=List[Badge])
async def get_badges(user=Depends(get_current_user)) -> List[Badge]:
    badges = BadgeRepository.get_all(user.id)
    return [Badge(**b) for b in badges]
