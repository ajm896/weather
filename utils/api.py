"""
api.py

Utility functions for fetching and caching weather forecast data from the National Weather Service (NWS) API.

This module provides functions to retrieve 12-hour and hourly forecasts, as well as raw gridpoint data, from the NWS API. It also includes utilities for caching and loading forecast data locally in JSON format. The module is designed to be used by other parts of the application to keep weather data up to date and accessible.

Constants:
    NWS_X, NWS_Y: Grid coordinates for the NWS API endpoint.
    BASE_URL: Base URL for the NWS gridpoint API.
    USER_AGENT: User agent string for API requests.
    CACHED_HOURLY_DATA, CACHED_FORCAST_DATA, CACHED_RAW_DATA: Filenames for cached data.

Functions:
    update_all_forecasts: Fetches and caches all forecast data from the NWS API.
    fetch_forecast: Fetches the latest 12-hour forecast data from the NWS API.
    fetch_hourly_forecast: Fetches the latest hourly forecast data from the NWS API.
    fetch_gridpoint_raw_data: Fetches the latest raw gridpoint data from the NWS API.
    load_cached_data: Loads cached forecast data from a file.
    cache_forecast: Saves forecast data to a file in JSON format.
"""

import requests
import json

BASE_URL = "https://api.weather.gov/gridpoints/GSP/"
USER_AGENT = "weather-learner/1.0"

GRID_POINTS = {
    "home": (40, 68),
    "work": (56, 70),
    "church": (34, 60),
    "ehhs": (61, 62),
}

CACHED_HOURLY_DATA = "cached_hourly_data.json"
CACHED_FORCAST_DATA = "cached_forecast_data.json"
CACHED_RAW_DATA = "cached_raw_data.json"


def update_all_forecasts(location: str) -> None:
    """
    Update all forecast data by fetching from the NWS API and caching the results locally.

    Fetches the latest 12-hour forecast, hourly forecast, and raw gridpoint data from the NWS API,
    then saves each to its respective cache file.
    """
    print("Fetching latest forecast data...")
    forecast_data = fetch_forecast(GRID_POINTS[location])
    hourly_forecast_data = fetch_hourly_forecast(GRID_POINTS[location])
    gridpoint_raw_data = fetch_gridpoint_raw_data(GRID_POINTS[location])

    cache_forecast(forecast_data, f"{location}_CACHED_FORCAST_DATA.json")
    cache_forecast(hourly_forecast_data, f"{location}_CACHED_HOURLY_DATA.json")
    cache_forecast(gridpoint_raw_data, f"{location}_CACHED_RAW_DATA.json")

    print("All forecasts updated.")


def fetch_forecast(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest 12-hour forecast data from the NWS API.

    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}/forecast",
        headers={"User-Agent": USER_AGENT},
    ).json()


def fetch_hourly_forecast(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest hourly forecast data from the NWS API.

    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}/forecast/hourly",
        headers={"User-Agent": USER_AGENT},
    ).json()


def fetch_gridpoint_raw_data(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest raw gridpoint forecast data from the NWS API.

    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}", headers={"User-Agent": USER_AGENT}
    ).json()


def load_cached_data(filename: str) -> dict[str, dict]:
    """
    Load cached forecast data from a file.

    Args:
        filename (str): The path to the cache file.
    Returns:
        dict[str, dict]: The cached data as a dictionary, or an empty dict if the file does not exist.
    """
    try:
        with open(filename, "r") as f:
            import json

            return json.load(f)
    except FileNotFoundError:
        return {}


def cache_forecast(forecast_data, filename) -> None:
    """
    Cache the forecast data to a file in JSON format.

    Args:
        forecast_data: The data to be cached (should be serializable to JSON).
        filename: The path to the cache file.
    """
    with open(filename, "w") as f:
        json.dump(forecast_data, f, indent=4)
    print("Forecast data saved to forecast.json")
