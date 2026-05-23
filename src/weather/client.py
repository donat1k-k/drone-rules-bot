import logging
import re

import aiohttp

logger = logging.getLogger(__name__)

_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
_COORD_RE = re.compile(r"^(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)$")


async def get_weather_for_location(raw: str) -> dict:
    raw = raw.strip()
    m = _COORD_RE.match(raw)
    if m:
        lat, lon = float(m.group(1)), float(m.group(2))
        location_name = f"{lat:.4f}, {lon:.4f}"
    else:
        geocoded = await _geocode(raw)
        if geocoded is None:
            return {"error": "not_found"}
        lat, lon, location_name = geocoded

    weather = await _fetch_weather(lat, lon)
    if weather is None:
        return {"error": "api_unavailable"}

    return {
        "location": location_name,
        "temp": weather["temperature_2m"],
        "wind": weather["wind_speed_10m"],
        "precip": weather["precipitation"],
        "assessment": _assess(weather["wind_speed_10m"], weather["precipitation"]),
    }


async def _geocode(city: str) -> tuple[float, float, str] | None:
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                _GEOCODING_URL,
                params={"name": city, "count": 1, "language": "ru", "format": "json"},
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning("Geocoding error: %s", e)
        return None

    results = data.get("results")
    if not results:
        return None
    r = results[0]
    country = r.get("country", "")
    name = f"{r.get('name', city)}, {country}" if country else r.get("name", city)
    return r["latitude"], r["longitude"], name


async def _fetch_weather(lat: float, lon: float) -> dict | None:
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                _FORECAST_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,wind_speed_10m,precipitation,weather_code",
                    "wind_speed_unit": "ms",
                },
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning("Weather API error: %s", e)
        return None

    c = data.get("current", {})
    return {
        "temperature_2m": c.get("temperature_2m", 0.0),
        "wind_speed_10m": c.get("wind_speed_10m", 0.0),
        "precipitation": c.get("precipitation", 0.0),
    }


def _assess(wind_ms: float, precipitation_mm: float) -> dict:
    if wind_ms >= 10 or precipitation_mm > 0:
        return {"emoji": "⛔", "text": "по погоде полёт лучше отложить"}
    if wind_ms >= 5:
        return {"emoji": "⚠️", "text": "условия требуют осторожности"}
    return {
        "emoji": "✅",
        "text": "погодные условия выглядят спокойными для тренировочного полёта",
    }
