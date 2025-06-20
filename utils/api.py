import requests
import json

NWS_X = 40
NWS_Y = 68
BASE_URL = f"https://api.weather.gov/gridpoints/GSP/{NWS_X},{NWS_Y}/"
USER_AGENT = "weather-learner/1.0"


def update_all_forecasts() -> None:
    """Update all forecast data by fetching from the NWS API."""
    print("Fetching latest forecast data...")
    forecast_data = fetch_forecast()
    hourly_forecast_data = fetch_hourly_forecast()
    gridpoint_raw_data = fetch_gridpoint_raw_data()

    cache_forecast(forecast_data, "forecast.json")
    cache_forecast(hourly_forecast_data, "hourly_forecast.json")
    cache_forecast(gridpoint_raw_data, "gridpoint_raw.json")

    print("All forecasts updated.")


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


def fetch_gridpoint_raw_data() -> dict[str, dict]:
    """Fetch the latest gridpoint forecast data from the NWS API."""
    return requests.get(BASE_URL, headers={"User-Agent": USER_AGENT}).json()


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
