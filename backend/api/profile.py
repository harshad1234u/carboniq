"""Module docstring."""
import os
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.client import get_supabase
from models.profile import ProfileCreate, ProfileResponse, AuthSignup, AuthLogin
from services.profile_service import create_profile, update_profile, get_profile
from utils.rate_limit import limiter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """

    Args:
      credentials: HTTPAuthorizationCredentials:  (Default value = Depends(security))

    Returns:

    """
    token = credentials.credentials
    client = get_supabase()
    try:
        response = client.auth.get_user(token)
        if response and response.user:
            return response.user
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


@router.post("/auth/signup")
@limiter.limit("5/minute")
async def signup(request: Request, auth_data: AuthSignup) -> dict:
    """Docstring."""
    client = get_supabase()
    try:
        response = client.auth.sign_up(
            {
                "email": auth_data.email,
                "password": auth_data.password,
                "options": {"data": {"name": auth_data.name}},
            }
        )
        return {"message": "User created", "user": response.user}
    except Exception as e:
        logger.error(f"Signup error: {e}")
        # Sanitize exception message so raw details are not exposed to client
        raise HTTPException(
            status_code=400,
            detail="Failed to create user account. Please check your credentials and try again.",
        )


@router.post("/auth/login")
@limiter.limit("10/minute")
async def login(request: Request, auth_data: AuthLogin) -> dict:
    """Docstring."""
    client = get_supabase()
    try:
        response = client.auth.sign_in_with_password(
            {"email": auth_data.email, "password": auth_data.password}
        )

        # Check if profile is complete
        profile_complete = False
        if response.user:
            prof = get_profile(response.user.id)
            if prof and prof.get("city"):
                profile_complete = True

        return {"session": response.session, "profile_complete": profile_complete}
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/profile", response_model=ProfileResponse)
async def get_user_profile(user=Depends(get_current_user)) -> dict:
    """Docstring."""
    profile = get_profile(user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/profile", response_model=ProfileResponse)
async def update_user_profile(
    profile_data: ProfileCreate, user=Depends(get_current_user)
) -> dict:
    """Docstring."""
    try:
        data = profile_data.model_dump()
        if not data.get("email"):
            data["email"] = user.email

        existing = get_profile(user.id)
        if existing:
            updated = update_profile(user.id, data)
        else:
            updated = create_profile(user.id, data)
        return updated
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(status_code=400, detail="Failed to update profile")
