"""
api.py

Utility functions for fetching, caching, and loading weather forecast data from the National Weather Service (NWS) API.

This module provides functions to retrieve 12-hour forecasts, hourly forecasts, and raw gridpoint data from the NWS API for multiple locations. It also includes utilities for caching and loading forecast data locally in JSON format, organized by location. The module is designed to be used by other parts of the application to keep weather data up to date and accessible.

Constants:
    BASE_URL: Base URL for the NWS gridpoint API.
    USER_AGENT: User agent string for API requests.
    GRID_POINTS: Dictionary mapping location names to NWS grid coordinates.
    CACHED_HOURLY_DATA, CACHED_FORCAST_DATA, CACHED_RAW_DATA: Default filenames for cached data (not location-specific).

Functions:
    update_all_forecasts(location): Fetches and caches all forecast data for a given location from the NWS API.
    fetch_forecast(location): Fetches the latest 12-hour forecast data for a location from the NWS API.
    fetch_hourly_forecast(location): Fetches the latest hourly forecast data for a location from the NWS API.
    fetch_gridpoint_raw_data(location): Fetches the latest raw gridpoint data for a location from the NWS API.
    load_cached_data(filename): Loads cached forecast data from a file in the data/ directory.
    cache_forecast(forecast_data, filename): Saves forecast data to a file in the data/ directory in JSON format.
"""

import logging
import requests
import json

from weather import models

# Base URL for NWS gridpoint API requests
BASE_URL = "https://api.weather.gov/gridpoints/GSP/"
# Identifier sent with HTTP requests
USER_AGENT = "weather-learner/1.0"

# Mapping from location labels to NWS grid coordinates
GRID_POINTS = {
    "home": (40, 68),
    "work": (56, 70),
    "church": (34, 60),
    "ehhs": (61, 62),
}

# Default filenames for cached responses
CACHED_HOURLY_DATA = "cached_hourly_data.json"
CACHED_FORCAST_DATA = "cached_forecast_data.json"
CACHED_RAW_DATA = "cached_raw_data.json"


def update_all_forecasts(location: str) -> None:
    """
    Update all forecast data by fetching from the NWS API and caching the results locally for a given location.

    Args:
        location (str): The location key (e.g., 'home', 'work', etc.) to fetch and cache forecasts for.

    This function fetches the latest 12-hour forecast, hourly forecast, and raw gridpoint data from the NWS API
    for the specified location, then saves each to its respective cache file in the data/ directory.
    """
    print("Fetching latest forecast data...")
    forecast_data = fetch_forecast(GRID_POINTS[location])
    hourly_forecast_data = fetch_hourly_forecast(GRID_POINTS[location])
    gridpoint_raw_data = fetch_gridpoint_raw_data(GRID_POINTS[location])

    cache_forecast(forecast_data, f"{location}_CACHED_FORECAST_DATA.json")
    cache_forecast(hourly_forecast_data, f"{location}_CACHED_HOURLY_DATA.json")
    cache_forecast(gridpoint_raw_data, f"{location}_CACHED_RAW_DATA.json")

    print("All forecasts updated.")


def fetch_forecast(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest 12-hour forecast data from the NWS API for a given location.

    Args:
        location (tuple[int, int]): The (x, y) grid coordinates for the NWS API endpoint.
    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}/forecast",
        headers={"User-Agent": USER_AGENT},
    ).json()


def fetch_hourly_forecast(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest hourly forecast data from the NWS API for a given location.

    Args:
        location (tuple[int, int]): The (x, y) grid coordinates for the NWS API endpoint.
    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}/forecast/hourly",
        headers={"User-Agent": USER_AGENT},
    ).json()


def fetch_gridpoint_raw_data(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest raw gridpoint forecast data from the NWS API for a given location.

    Args:
        location (tuple[int, int]): The (x, y) grid coordinates for the NWS API endpoint.
    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}", headers={"User-Agent": USER_AGENT}
    ).json()


def load_cached_data(filename: str) -> models.ForecastData | None:
    """
    Load cached forecast data from a file in the data/ directory.

    Args:
        filename (str): The name of the cache file (relative to the data/ directory).
    Returns:
        models.ForecastData: The cached data as a ForecastData object, or None if the file does not exist.
    """
    try:
        with open(f"data/{filename}", "r") as f:
            import json

            raw_data = json.load(f)

            # Determine the forecast type based on filename pattern and create appropriate model
            if "FORCAST_DATA" in filename:  # 12-hour forecast
                geojson_data = models.Gridpoint12hForecastGeoJson(**raw_data)
                return models.ForecastData(type="12h", data=geojson_data)
            elif "HOURLY_DATA" in filename:  # Hourly forecast
                hourly_geojson_data = models.GridpointHourlyForecastGeoJson(**raw_data)
                return models.ForecastData(type="hourly", data=hourly_geojson_data)
            elif "RAW_DATA" in filename:  # Raw gridpoint data
                raw_geojson_data = models.GridpointGeoJson(**raw_data)
                return models.ForecastData(type="gridpoint", data=raw_geojson_data)
            else:
                # Default to 12h forecast if pattern doesn't match
                default_geojson_data = models.Gridpoint12hForecastGeoJson(**raw_data)
                return models.ForecastData(type="12h", data=default_geojson_data)

    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Error loading cached data from {filename}: {e}")
        return None


def cache_forecast(forecast_data, filename) -> None:
    """
    Cache the forecast data to a file in JSON format in the data/ directory.

    Args:
        forecast_data: The data to be cached (should be serializable to JSON).
        filename: The name of the cache file (relative to the data/ directory).
    """
    with open(f"data/{filename}", "w") as f:
        json.dump(forecast_data, f, indent=4)
    logging.log(msg=f"Forecast data saved to {filename}", level=logging.INFO)
