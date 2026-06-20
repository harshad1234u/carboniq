"""
CarbonIQ Configuration Module.

Loads environment variables using python-dotenv and validates that all
required configuration values are present. Exports a singleton Settings
object used throughout the application.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from the backend directory (one level up from utils/)
# ---------------------------------------------------------------------------
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)


class ConfigError(Exception):
    """Raised when a required configuration variable is missing."""


@dataclass(frozen=True)
class Settings:
    """Application-wide settings sourced from environment variables.

    Attributes:
        gemini_api_key: Google Gemini API key for AI coach features.
        openweather_api_key: OpenWeather API key for weather lookups.
        supabase_url: URL of the Supabase project instance.
        supabase_service_role_key: Supabase service-role key for admin operations.
        supabase_jwt_secret: Secret used to validate Supabase JWTs.
        app_env: Current environment (development | staging | production).
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """

    gemini_api_key: str = ""
    openweather_api_key: str = ""
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""
    app_env: str = "development"
    log_level: str = "INFO"


def _get_env(name: str, required: bool = True, default: str = "") -> str:
    """Retrieve an environment variable, raising if required and missing.

    Args:
        name: The environment variable name.
        required: Whether the variable is mandatory.
        default: Fallback value when the variable is not required.

    Returns:
        The value of the environment variable.

    Raises:
        ConfigError: If the variable is required but missing or empty.
    """
    value = os.getenv(name, default).strip()
    if required and not value:
        raise ConfigError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.example to .env and fill in all values."
        )
    return value


def load_settings() -> Settings:
    """Build a ``Settings`` instance from environment variables.

    Returns:
        A fully-populated ``Settings`` dataclass.

    Raises:
        ConfigError: If any required variable is absent.
    """
    return Settings(
        gemini_api_key=_get_env("GEMINI_API_KEY"),
        openweather_api_key=_get_env("OPENWEATHER_API_KEY"),
        supabase_url=_get_env("SUPABASE_URL"),
        supabase_service_role_key=_get_env("SUPABASE_SERVICE_ROLE_KEY"),
        supabase_jwt_secret=_get_env("SUPABASE_JWT_SECRET"),
        app_env=_get_env("APP_ENV", required=False, default="development"),
        log_level=_get_env("LOG_LEVEL", required=False, default="INFO"),
    )


def load_settings_safe() -> Settings:
    """Load settings without raising on missing vars.

    Useful during testing or when only a subset of services is needed.

    Returns:
        A ``Settings`` instance with whatever values are available.
    """
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY", ""),
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
        supabase_jwt_secret=os.getenv("SUPABASE_JWT_SECRET", ""),
        app_env=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


# ---------------------------------------------------------------------------
# Singleton – import ``settings`` from here in other modules.
# In production the app calls ``load_settings()`` at startup; unit tests can
# import ``load_settings_safe()`` to avoid ConfigError.
# ---------------------------------------------------------------------------
try:
    settings: Settings = load_settings()
except ConfigError:
    # Graceful degradation so that imports don't explode during testing.
    settings = load_settings_safe()
