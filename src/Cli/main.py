"""Command line interface for the weather utilities.

This module fetches forecasts from the National Weather Service API,
caches them locally and prints summaries. Several predefined locations
are available.

Functions
---------
``_print_hourly(data)`` – print a summary of hourly forecast data.
``_print_daily(data)`` – print a summary of 12‑hour forecast data.
``main(argv)`` – entry point that parses arguments and dispatches commands.

Usage
-----
``python -m Cli.main {update-all, show-hourly, show-daily} [--location
LOCATION]``
"""

from __future__ import annotations

import argparse
from typing import Optional

from weather import api
from weather.models import ForecastData

# Mapping from location labels to NWS grid coordinates
# used throughout the CLI.
GRID_POINTS = {
    "home": (40, 68),
    "work": (56, 70),
    "church": (34, 60),
    "ehhs": (61, 62),
}


def _print_hourly(data: ForecastData) -> None:
    """
    Print a simple summary of hourly forecast data to the console.

    Args:
        data (dict): The forecast data dictionary as returned by the API.
    """
    periods = getattr(getattr(data, "properties", {}), "periods", [])
    for period in periods:
        temp = period.get("temperature")
        unit = period.get("temperatureUnit")
        short = period.get("shortForecast")
        start = period.get("startTime")
        print(f"{start}: {temp}{unit} - {short}")


def _print_daily(data: ForecastData) -> None:
    """
    Print a simple summary of 12-hour forecast data to the console.

    Args:
        data (dict): The forecast data dictionary as returned by the API.
    """
    periods = getattr(getattr(data, "properties", {}), "periods", [])
    for period in periods:
        name = period.get("name")
        temp = period.get("temperature")
        unit = period.get("temperatureUnit")
        short = period.get("shortForecast")
        print(f"{name}: {temp}{unit} - {short}")


def main(argv: Optional[list[str]] = None) -> None:
    """
    Entry point for the CLI. Parses command-line arguments and dispatches to
    the appropriate command.

    Args:
        argv (Optional[list[str]]): List of command-line arguments. If None,
            uses ``sys.argv``.
    """
    parser = argparse.ArgumentParser(description="weather forecast utilities")

    sub_cmd = parser.add_subparsers(dest="command")

    # Add subparsers and move --location to each
    update_all_parser = sub_cmd.add_parser(
        "update-all", help="Fetch and cache all forecasts"
    )
    update_all_parser.add_argument(
        "-l",
        "--location",
        choices=GRID_POINTS.keys(),
        default="home",
        help="Location to fetch the forecast for",
    )

    show_hourly_parser = sub_cmd.add_parser(
        "show-hourly", help="Display the latest hourly forecast"
    )
    show_hourly_parser.add_argument(
        "-l",
        "--location",
        choices=GRID_POINTS.keys(),
        default="home",
        help="Location to fetch the forecast for",
    )

    show_daily_parser = sub_cmd.add_parser(
        "show-daily", help="Display the latest 12h forecast"
    )
    show_daily_parser.add_argument(
        "-l",
        "--location",
        choices=GRID_POINTS.keys(),
        default="home",
        help="Location to fetch the forecast for",
    )

    args = parser.parse_args(argv)

    if args.command == "update-all":
        api.update_all_forecasts(["home", "work", "church", "ehhs"])
    elif args.command == "show-hourly":
        data = api.load_cached_data(f"{args.location}_CACHED_HOURLY_DATA.json")
        if data is not None:
            _print_hourly(data)
        else:
            print("No cached hourly data found for the selected location.")
    elif args.command == "show-daily":
        cache_file = f"{args.location}_CACHED_FORCAST_DATA.json"
        data = api.load_cached_data(cache_file)
        if data is not None:
            _print_daily(data)
        else:
            print("No cached daily data found for the selected location.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
