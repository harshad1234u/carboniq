import pytest
from httpx import HTTPStatusError, RequestError
from services.weather_service import get_weather, clear_cache, _CACHE, _default_weather
from utils.config import settings

@pytest.fixture(autouse=True)
def setup_weather_test():
    clear_cache()
    original_key = settings.openweather_api_key
    object.__setattr__(settings, 'openweather_api_key', 'fake_key')
    yield
    object.__setattr__(settings, 'openweather_api_key', original_key)
    clear_cache()

@pytest.mark.asyncio
async def test_get_weather_missing_key():
    object.__setattr__(settings, 'openweather_api_key', '')
    weather = await get_weather("London")
    assert weather.city == "London"
    assert weather.temperature == 25.0
    assert weather.description == "Moderate"

@pytest.mark.asyncio
async def test_get_weather_fallback_on_exception(mocker):
    # Mock httpx.AsyncClient.get to raise RequestError
    mocker.patch("httpx.AsyncClient.get", side_effect=RequestError("Network error"))
    weather = await get_weather("Mumbai")
    assert weather.city == "Mumbai"
    assert weather.temperature == 25.0
    
@pytest.mark.asyncio
async def test_get_weather_success(mocker):
    class MockResponse:
        def json(self):
            return {
                "name": "Delhi",
                "main": {"temp": 30.5, "humidity": 70},
                "weather": [{"description": "clear sky", "icon": "01d"}]
            }
        def raise_for_status(self):
            pass

    mocker.patch("httpx.AsyncClient.get", return_value=MockResponse())
    weather = await get_weather("Delhi")
    assert weather.city == "Delhi"
    assert weather.temperature == 30.5
    assert weather.humidity == 70
    assert weather.description == "clear sky"
