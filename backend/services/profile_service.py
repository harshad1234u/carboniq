"""Module docstring."""
import logging
from typing import Any, Dict, Optional
from database.repositories import ProfileRepository

logger = logging.getLogger(__name__)


def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Fetch user profile.

    Args:
      user_id: str: 

    Returns:

    """
    try:
        return ProfileRepository.get_profile(user_id)
    except Exception as e:
        logger.error(f"Error fetching profile for {user_id}: {e}")
        return None


def create_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new profile.

    Args:
      user_id: str: 
      profile_data: Dict[str: 
      Any]: 

    Returns:

    """
    try:
        data = profile_data.copy()
        data["id"] = user_id
        return ProfileRepository.create_profile(data)
    except Exception as e:
        logger.error(f"Error creating profile for {user_id}: {e}")
        raise ValueError("Failed to create profile")


def update_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing profile.

    Args:
      user_id: str: 
      profile_data: Dict[str: 
      Any]: 

    Returns:

    """
    try:
        return ProfileRepository.update_profile(user_id, profile_data)
    except Exception as e:
        logger.error(f"Error updating profile for {user_id}: {e}")
        raise ValueError("Failed to update profile")
