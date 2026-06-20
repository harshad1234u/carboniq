"""
CarbonIQ Weather Service.

Fetches current weather data from the OpenWeather API with a simple
in-memory cache (TTL 30 minutes).  Falls back to a sensible default
when the API is unreachable.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from models.weather import WeatherData
from utils.config import settings

logger = logging.getLogger("carboniq.weather")

# ---------------------------------------------------------------------------
# Simple in-memory cache  { city_lower: (WeatherData, timestamp) }
# ---------------------------------------------------------------------------
_CACHE: dict[str, tuple[WeatherData, float]] = {}
_CACHE_TTL_SECONDS: int = 30 * 60  # 30 minutes

_OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def _default_weather(city: str) -> WeatherData:
    """Return a safe fallback weather response.

    Args:
      city: The requested city name
      city: str: 

    Returns:
      A ``WeatherData`` with moderate/neutral defaults.

    """
    return WeatherData(
        city=city,
        temperature=25.0,
        description="Moderate",
        humidity=60,
        icon="01d",
    )


async def get_weather(city: str) -> WeatherData:
    """Fetch current weather for *city* from OpenWeather.

    Results are cached for 30 minutes.  If the API call fails for any reason
    (network error, invalid key, quota exhausted) a fallback ``WeatherData``
    with neutral values is returned so that downstream services are never
    blocked.

    Args:
        city: City name (e.g. ``"Mumbai"``).

    Returns:
        A ``WeatherData`` instance.
    """
    cache_key = city.strip().lower()

    # --- Check cache ---
    if cache_key in _CACHE:
        cached_data, cached_at = _CACHE[cache_key]
        if time.time() - cached_at < _CACHE_TTL_SECONDS:
            logger.debug("Weather cache hit for %s", city)
            return cached_data

    # --- Call OpenWeather API ---
    api_key = settings.openweather_api_key
    if not api_key:
        logger.warning("OpenWeather API key not configured; returning default.")
        return _default_weather(city)

    params: dict[str, Any] = {
        "q": city.strip(),
        "appid": api_key,
        "units": "metric",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(_OPENWEATHER_URL, params=params)
            response.raise_for_status()
            data = response.json()

        weather = WeatherData(
            city=data.get("name", city),
            temperature=float(data.get("main", {}).get("temp", 25)),
            description=data.get("weather", [{}])[0].get("description", "N/A"),
            humidity=int(data.get("main", {}).get("humidity", 60)),
            icon=data.get("weather", [{}])[0].get("icon", "01d"),
        )

        # Update cache
        _CACHE[cache_key] = (weather, time.time())
        logger.info("Weather fetched and cached for %s", city)
        return weather

    except httpx.HTTPStatusError as exc:
        logger.warning(
            "OpenWeather HTTP %s for city '%s': %s",
            exc.response.status_code,
            city,
            exc.response.text[:200],
        )
    except httpx.RequestError as exc:
        logger.warning("OpenWeather request failed for '%s': %s", city, exc)
    except Exception as exc:
        logger.error("Unexpected error fetching weather for '%s': %s", city, exc)

    return _default_weather(city)


def clear_cache() -> None:
    """Clear the weather cache (useful for testing)."""
    _CACHE.clear()
