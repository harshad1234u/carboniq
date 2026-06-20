"""Module docstring."""
import logging
from typing import Any, Dict, List, Optional
from database.client import get_supabase

logger = logging.getLogger(__name__)


class ProfileRepository:
    """ """
    @staticmethod
    def get_profile(user_id: str) -> Optional[Dict[str, Any]]:
        """

        Args:
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        response = client.table("profiles").select("*").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    def create_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
          profile_data: Dict[str: 
          Any]: 

        Returns:

        """
        client = get_supabase()
        response = client.table("profiles").insert(profile_data).execute()
        return response.data[0]

    @staticmethod
    def update_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
          user_id: str: 
          profile_data: Dict[str: 
          Any]: 

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("profiles").update(profile_data).eq("id", user_id).execute()
        )
        return response.data[0]


class CarbonRepository:
    """ """
    @staticmethod
    def create_entry(entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
          entry_data: Dict[str: 
          Any]: 

        Returns:

        """
        client = get_supabase()
        response = client.table("carbon_entries").insert(entry_data).execute()
        return response.data[0]

    @staticmethod
    def get_history(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """

        Args:
          user_id: str: 
          limit: int:  (Default value = 10)

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("carbon_entries")
            .select("*")
            .eq("profile_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data

    @staticmethod
    def get_latest(user_id: str) -> Optional[Dict[str, Any]]:
        """

        Args:
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("carbon_entries")
            .select("*")
            .eq("profile_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None


class RecommendationRepository:
    """ """
    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
          data: Dict[str: 
          Any]: 

        Returns:

        """
        client = get_supabase()
        response = client.table("recommendations").insert(data).execute()
        return response.data[0]

    @staticmethod
    def get_latest(user_id: str) -> Optional[Dict[str, Any]]:
        """

        Args:
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("recommendations")
            .select("*")
            .eq("profile_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None


class EcoPredictionRepository:
    """ """
    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
          data: Dict[str: 
          Any]: 

        Returns:

        """
        client = get_supabase()
        response = client.table("eco_predictions").insert(data).execute()
        return response.data[0]

    @staticmethod
    def get_latest(user_id: str) -> Optional[Dict[str, Any]]:
        """

        Args:
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("eco_predictions")
            .select("*")
            .eq("profile_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None


class ChallengeRepository:
    """ """
    @staticmethod
    def create_challenges(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """

        Args:
          data_list: List[Dict[str: 
          Any]]: 

        Returns:

        """
        client = get_supabase()
        response = client.table("challenges").insert(data_list).execute()
        return response.data

    @staticmethod
    def get_current(user_id: str) -> List[Dict[str, Any]]:
        """

        Args:
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        # simplified check for current week
        response = (
            client.table("challenges")
            .select("*")
            .eq("profile_id", user_id)
            .order("created_at", desc=True)
            .limit(3)
            .execute()
        )
        return response.data

    @staticmethod
    def complete_challenge(challenge_id: str, user_id: str) -> Dict[str, Any]:
        """

        Args:
          challenge_id: str: 
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("challenges")
            .update({"is_completed": True})
            .eq("id", challenge_id)
            .eq("profile_id", user_id)
            .execute()
        )
        return response.data[0]


class BadgeRepository:
    """ """
    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        """

        Args:
          data: Dict[str: 
          Any]: 

        Returns:

        """
        client = get_supabase()
        response = client.table("badges").insert(data).execute()
        return response.data[0]

    @staticmethod
    def get_all(user_id: str) -> List[Dict[str, Any]]:
        """

        Args:
          user_id: str: 

        Returns:

        """
        client = get_supabase()
        response = (
            client.table("badges")
            .select("*")
            .eq("profile_id", user_id)
            .order("earned_at", desc=True)
            .execute()
        )
        return response.data
