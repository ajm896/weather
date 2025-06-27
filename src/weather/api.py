"""Helpers for fetching and caching weather forecasts.

This module wraps the National Weather Service API. It can retrieve hourly
and 12-hour forecasts as well as raw gridpoint data. Responses are cached to
``data/`` for later use.

Constants
---------
``BASE_URL`` – base URL for the NWS gridpoint API
``USER_AGENT`` – user agent string for requests
``GRID_POINTS`` – mapping of location names to NWS coordinates
``CACHED_HOURLY_DATA`` – default hourly forecast cache file
``CACHED_FORCAST_DATA`` – default 12-hour forecast cache file
``CACHED_RAW_DATA`` – default raw gridpoint cache file

Key Functions
-------------
``update_all_forecasts(location)`` – fetch and cache all data for a location
``fetch_forecast(location)`` – get the latest 12-hour forecast
``fetch_hourly_forecast(location)`` – get the hourly forecast
``fetch_gridpoint_raw_data(location)`` – get raw gridpoint data
``load_cached_data(filename)`` – load cached forecast data
``cache_forecast(data, filename)`` – save forecast data to ``data/``
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


def update_all_forecasts(locations: list[str]) -> None:
    """
    Update all forecast data by fetching from the NWS API and caching the
    results locally for a given location.

    Args:
        location (str): The location key (e.g., 'home', 'work', etc.) to fetch
            and cache forecasts for.

    This function fetches the latest 12-hour forecast, hourly forecast and raw
    gridpoint data from the NWS API for the specified location, then saves each
    to its respective cache file in the ``data/`` directory.
    """
    for location in locations:
        if location not in GRID_POINTS:
            logging.error(f"Unknown location: {location}")
            continue

        print(f"Fetching latest forecast data for {location}...")
        forecast_data = _fetch_forecast(GRID_POINTS[location])
        hourly_forecast_data = _fetch_hourly_forecast(GRID_POINTS[location])
        gridpoint_raw_data = _fetch_gridpoint_raw_data(GRID_POINTS[location])

        _cache_forecast(forecast_data, f"{location}_CACHED_FORECAST_DATA.json")
        _cache_forecast(hourly_forecast_data, f"{location}_CACHED_HOURLY_DATA.json")
        _cache_forecast(gridpoint_raw_data, f"{location}_CACHED_RAW_DATA.json")

    print("All forecasts updated.")


def _fetch_forecast(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest 12-hour forecast data from the NWS API for a
    given location.

    Args:
        location (tuple[int, int]): The (x, y) grid coordinates for the
            NWS API endpoint.
    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}/forecast",
        headers={"User-Agent": USER_AGENT},
    ).json()


def _fetch_hourly_forecast(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest hourly forecast data from the NWS API for a
    given location.

    Args:
        location (tuple[int, int]): The (x, y) grid coordinates for the
            NWS API endpoint.
    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}/forecast/hourly",
        headers={"User-Agent": USER_AGENT},
    ).json()


def _fetch_gridpoint_raw_data(location: tuple[int, int]) -> dict[str, dict]:
    """
    Fetch the latest raw gridpoint forecast data from the NWS API for a
    given location.

    Args:
        location (tuple[int, int]): The (x, y) grid coordinates for the
            NWS API endpoint.
    Returns:
        dict[str, dict]: The JSON response from the API as a dictionary.
    """
    return requests.get(
        f"{BASE_URL}{location[0]},{location[1]}",
        headers={"User-Agent": USER_AGENT},
    ).json()


def load_cached_data(filename: str) -> models.ForecastData | None:
    """
    Load cached forecast data from a file in the data/ directory.

    Args:
        filename (str): The name of the cache file relative to the
            ``data/`` directory.
    Returns:
        models.ForecastData: The cached data as a ``ForecastData`` object, or
            ``None`` if the file does not exist.
    """
    try:
        with open(f"data/{filename}", "r") as f:
            import json

            raw_data = json.load(f)

            # Determine the forecast type based on the filename pattern and
            # create the appropriate model
            if "FORCAST_DATA" in filename:  # 12-hour forecast
                geojson_data = models.Gridpoint12hForecastGeoJson(**raw_data)
                return models.ForecastData(kind="12h", data=geojson_data)
            elif "HOURLY_DATA" in filename:  # Hourly forecast
                hourly_geojson_data = models.GridpointHourlyForecastGeoJson(**raw_data)
                return models.ForecastData(kind="hourly", data=hourly_geojson_data)
            elif "RAW_DATA" in filename:  # Raw gridpoint data
                raw_geojson_data = models.GridpointGeoJson(**raw_data)
                return models.ForecastData(kind="gridpoint", data=raw_geojson_data)
            else:
                # Default to 12h forecast if pattern doesn't match
                default_geojson_data = models.Gridpoint12hForecastGeoJson(**raw_data)
                return models.ForecastData(kind="12h", data=default_geojson_data)

    except FileNotFoundError:
        return None
    except Exception as e:
        logging.error(f"Error loading cached data from {filename}: {e}")
        return None


def _cache_forecast(forecast_data, filename) -> None:
    """
    Cache the forecast data to a file in JSON format in the data/ directory.

    Args:
        forecast_data: The data to be cached (should be serializable to JSON).
        filename: The name of the cache file (relative to the data/ directory).
    """
    with open(f"data/{filename}", "w") as f:
        json.dump(forecast_data, f, indent=4)
    logging.log(msg=f"Forecast data saved to {filename}", level=logging.INFO)
