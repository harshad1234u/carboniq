"""Tests for CarbonIQ Profile Service."""

import pytest
from unittest.mock import MagicMock, patch
from services.profile_service import get_profile, create_profile, update_profile


class TestGetProfile:
    """ """
    @patch("services.profile_service.ProfileRepository")
    def test_returns_profile_data(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.get_profile.return_value = {
            "id": "user-1",
            "name": "Test User",
            "email": "test@example.com",
            "city": "Mumbai",
        }
        result = get_profile("user-1")
        assert result is not None
        assert result["name"] == "Test User"
        mock_repo.get_profile.assert_called_once_with("user-1")

    @patch("services.profile_service.ProfileRepository")
    def test_returns_none_on_exception(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.get_profile.side_effect = Exception("DB error")
        result = get_profile("user-1")
        assert result is None

    @patch("services.profile_service.ProfileRepository")
    def test_returns_none_when_not_found(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.get_profile.return_value = None
        result = get_profile("nonexistent")
        assert result is None


class TestCreateProfile:
    """ """
    @patch("services.profile_service.ProfileRepository")
    def test_creates_profile_successfully(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        profile_data = {
            "name": "New User",
            "email": "new@example.com",
            "city": "Delhi",
            "transport_type": "bus",
            "diet_type": "vegetarian",
        }
        mock_repo.create_profile.return_value = {**profile_data, "id": "user-1"}
        result = create_profile("user-1", profile_data)
        assert result["id"] == "user-1"
        # Verify that user_id was added to the data
        call_args = mock_repo.create_profile.call_args[0][0]
        assert call_args["id"] == "user-1"

    @patch("services.profile_service.ProfileRepository")
    def test_raises_value_error_on_db_failure(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.create_profile.side_effect = Exception("DB write error")
        with pytest.raises(ValueError, match="Failed to create profile"):
            create_profile("user-1", {"name": "Test"})

    @patch("services.profile_service.ProfileRepository")
    def test_does_not_mutate_input_data(self, mock_repo):
        """Original profile_data dict should not be modified.

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.create_profile.return_value = {}
        original = {"name": "Test", "email": "t@t.com"}
        original_copy = original.copy()
        create_profile("user-1", original)
        assert original == original_copy  # Original unchanged


class TestUpdateProfile:
    """ """
    @patch("services.profile_service.ProfileRepository")
    def test_updates_profile_successfully(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        updated_data = {"name": "Updated Name", "city": "Bangalore"}
        mock_repo.update_profile.return_value = {
            "id": "user-1",
            **updated_data,
        }
        result = update_profile("user-1", updated_data)
        assert result["name"] == "Updated Name"
        mock_repo.update_profile.assert_called_once_with("user-1", updated_data)

    @patch("services.profile_service.ProfileRepository")
    def test_raises_value_error_on_db_failure(self, mock_repo):
        """

        Args:
          mock_repo: 

        Returns:

        """
        mock_repo.update_profile.side_effect = Exception("DB error")
        with pytest.raises(ValueError, match="Failed to update profile"):
            update_profile("user-1", {"name": "Test"})
