"""Module docstring."""
import logging
from fastapi import APIRouter, Depends, HTTPException
from api.profile import get_current_user
from models.calculator import CarbonInput, CarbonResult
from models.ai_coach import AiCoachResponse
from models.weather import WeatherData
from models.eco_twin import EcoTwinResponse, EcoTwinRequest
from services.carbon_calculator import calculate_emissions, calculate_carbon_score
from services.impact_equivalent_service import calculate_equivalents
from services.weather_service import get_weather
from services.ai_coach_service import get_recommendations
from services.eco_twin_service import calculate_eco_twin
from services.profile_service import get_profile
from database.repositories import (
    CarbonRepository,
    RecommendationRepository,
    EcoPredictionRepository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/carbon")


@router.post("/calculate", response_model=CarbonResult)
async def calculate_carbon(
    input_data: CarbonInput, user=Depends(get_current_user)
) -> CarbonResult:
    """Docstring."""
    try:
        # Calculate emissions
        result = calculate_emissions(input_data)

        # Save to database
        entry_data = input_data.model_dump()
        entry_data["profile_id"] = user.id
        entry_data["transport_emissions"] = result.transport_emissions
        entry_data["electricity_emissions"] = result.electricity_emissions
        entry_data["food_emissions"] = result.food_emissions
        entry_data["flight_emissions"] = result.flight_emissions
        entry_data["total_emissions"] = result.total_emissions
        entry_data["carbon_score"] = result.carbon_score.score
        entry_data["carbon_level"] = result.carbon_score.level

        CarbonRepository.create_entry(entry_data)

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        raise HTTPException(status_code=400, detail="Failed to calculate emissions")


@router.get("/weather/{city}", response_model=WeatherData)
async def get_city_weather(city: str, user=Depends(get_current_user)) -> WeatherData:
    """Docstring."""
    weather = await get_weather(city)
    return weather


@router.post("/ai-coach", response_model=AiCoachResponse)
async def run_ai_coach(user=Depends(get_current_user)) -> AiCoachResponse:
    """Docstring."""
    try:
        profile = get_profile(user.id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        latest_entry = CarbonRepository.get_latest(user.id)
        if not latest_entry:
            raise HTTPException(status_code=400, detail="No carbon entry found")

        # Reconstruct CarbonResult from entry
        carbon_score = calculate_carbon_score(latest_entry["total_emissions"])
        impact = calculate_equivalents(latest_entry["total_emissions"])
        footprint = CarbonResult(
            transport_emissions=latest_entry["transport_emissions"],
            electricity_emissions=latest_entry["electricity_emissions"],
            food_emissions=latest_entry["food_emissions"],
            flight_emissions=latest_entry["flight_emissions"],
            total_emissions=latest_entry["total_emissions"],
            carbon_score=carbon_score,
            impact_equivalents=impact,
        )

        weather = await get_weather(profile.get("city", "London"))

        response = await get_recommendations(footprint, weather, profile)

        # Store recommendations
        RecommendationRepository.create(
            {
                "profile_id": user.id,
                "entry_id": latest_entry["id"],
                "recommendations": [r.model_dump() for r in response.recommendations],
                "weather_context": (
                    response.weather_context.model_dump()
                    if response.weather_context
                    else None
                ),
                "total_co2_savings": response.total_co2_savings,
                "total_cost_savings": response.total_cost_savings,
            }
        )

        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI Coach error: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate recommendations"
        )


@router.post("/eco-twin", response_model=EcoTwinResponse)
async def run_eco_twin(
    request: EcoTwinRequest, user=Depends(get_current_user)
) -> EcoTwinResponse:
    """Docstring."""
    try:
        latest_entry = CarbonRepository.get_latest(user.id)
        if not latest_entry:
            raise HTTPException(status_code=400, detail="No carbon entry found")

        latest_recs = RecommendationRepository.get_latest(user.id)
        if not latest_recs:
            raise HTTPException(
                status_code=400, detail="No recommendations found. Run AI Coach first."
            )

        # Optional: filter by recommendation_id if provided in request

        from models.ai_coach import Recommendation

        recs_list = [Recommendation(**r) for r in latest_recs["recommendations"]]

        response = calculate_eco_twin(latest_entry["total_emissions"], recs_list)

        # Store prediction
        EcoPredictionRepository.create(
            {
                "profile_id": user.id,
                "entry_id": latest_entry["id"],
                "current_footprint": response.current_footprint,
                "predicted_footprint": response.predicted_footprint,
                "reduction_percentage": response.reduction_percentage,
                "impact_equivalents": response.predicted_equivalents,
                "recommendation_impacts": response.recommendation_impacts,
            }
        )

        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Eco Twin error: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate Eco Twin prediction"
        )
