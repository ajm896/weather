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

NWS_X = 40
NWS_Y = 68
BASE_URL = f"https://api.weather.gov/gridpoints/GSP/{NWS_X},{NWS_Y}/"
USER_AGENT = "weather-learner/1.0"

CACHED_HOURLY_DATA = "cached_hourly_data.json"
CACHED_FORCAST_DATA = "cached_forecast_data.json"
CACHED_RAW_DATA = "cached_raw_data.json"


def update_all_forecasts() -> None:
    """
    Update all forecast data by fetching from the NWS API and caching the results locally.

    Fetches the latest 12-hour forecast, hourly forecast, and raw gridpoint data from the NWS API,
    then saves each to its respective cache file.
    """
    print("Fetching latest forecast data...")
    forecast_data = fetch_forecast()
    hourly_forecast_data = fetch_hourly_forecast()
    gridpoint_raw_data = fetch_gridpoint_raw_data()

    cache_forecast(forecast_data, CACHED_FORCAST_DATA)
    cache_forecast(hourly_forecast_data, CACHED_HOURLY_DATA)
    cache_forecast(gridpoint_raw_data, CACHED_RAW_DATA)

    print("All forecasts updated.")


def fetch_forecast() -> dict[str, dict]:
    """
    Fetch the latest 12-hour forecast data from the NWS API.

    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        BASE_URL + "forecast", headers={"User-Agent": USER_AGENT}
    ).json()


def fetch_hourly_forecast() -> dict[str, dict]:
    """
    Fetch the latest hourly forecast data from the NWS API.

    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        BASE_URL + "forecast", headers={"User-Agent": USER_AGENT}
    ).json()


def fetch_gridpoint_raw_data() -> dict[str, dict]:
    """
    Fetch the latest raw gridpoint forecast data from the NWS API.

    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(BASE_URL, headers={"User-Agent": USER_AGENT}).json()


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
