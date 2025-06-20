import requests, json
import pandas as pd

NWS_X = 40
NWS_Y = 68
BASE_URL = f"https://api.weather.gov/gridpoints/GSP/{NWS_X},{NWS_Y}/"
USER_AGENT = "weather-learner/1.0"


def fetch_forecast() -> dict[str, dict]:
    """Fetch the latest forecast data from the NWS API."""
    return requests.get(
        BASE_URL + "forecast", headers={"User-Agent": USER_AGENT}
    ).json()


def fetch_hourly_forecast() -> dict[str, dict]:
    """Fetch the latest hourly forecast data from the NWS API."""
    return requests.get(
        BASE_URL + "forecast", headers={"User-Agent": USER_AGENT}
    ).json()


def load_cached_data(filename: str) -> dict[str, dict]:
    """Load cached forecast data from a file."""
    try:
        with open(filename, "r") as f:
            import json

            return json.load(f)
    except FileNotFoundError:
        return {}


def cache_forecast(forecast_data, filename) -> None:
    """Cache the forecast data to a file."""
    with open(filename, "w") as f:
        json.dump(forecast_data, f, indent=4)
    print("Forecast data saved to forecast.json")
