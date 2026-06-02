from __future__ import annotations
from typing import Any
import requests
from tools._shared import TIMEOUT, err

def get_weather(location: str = "") -> dict[str, Any]:
    """
    Get the current weather of a location using wttr.in.
    """
    if not location:
        return {"tool": "weather", "error": "Missing location argument"}
    try:
        url = f"https://wttr.in/{location}"
        resp = requests.get(url, params={"format": "j1"}, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        current = data.get("current_condition", [{}])[0]
        temp_c = current.get("temp_C")
        desc = current.get("weatherDesc", [{}])[0].get("value")
        humidity = current.get("humidity")
        wind = current.get("windspeedKmph")
        
        return {
            "tool": "weather",
            "location": location,
            "temperature_celsius": temp_c,
            "description": desc,
            "humidity_percent": humidity,
            "wind_speed_kmh": wind,
            "source": "wttr.in"
        }
    except Exception as exc:
        return err("weather", exc)
