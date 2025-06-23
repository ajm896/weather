"""
Command line interface for the weather utilities.

This module provides a CLI for interacting with weather forecast data using the utilities in utils.api. It allows users to fetch and cache forecasts, and display hourly or daily summaries for predefined locations.

Functions:
    _print_hourly(data): Print a summary of hourly forecast data.
    _print_daily(data): Print a summary of 12-hour forecast data.
    main(argv): Entry point for the CLI, parses arguments and dispatches commands.

Usage:
    python main.py [--location LOCATION] {update-all, show-hourly, show-daily}
"""

from __future__ import annotations

import argparse
from typing import Optional

from utils import api

# Mapping from location labels to NWS grid coordinates
# used throughout the CLI.
GRID_POINTS = {
    "home": (40, 68),
    "work": (56, 70),
    "church": (34, 60),
    "ehhs": (61, 62),
}


def _print_hourly(data: dict) -> None:
    """
    Print a simple summary of hourly forecast data to the console.

    Args:
        data (dict): The forecast data dictionary as returned by the API.
    """
    periods = data.get("properties", {}).get("periods", [])
    for period in periods:
        temp = period.get("temperature")
        unit = period.get("temperatureUnit")
        short = period.get("shortForecast")
        start = period.get("startTime")
        print(f"{start}: {temp}{unit} - {short}")


def _print_daily(data: dict) -> None:
    """
    Print a simple summary of 12-hour forecast data to the console.

    Args:
        data (dict): The forecast data dictionary as returned by the API.
    """
    periods = data.get("properties", {}).get("periods", [])
    for period in periods:
        name = period.get("name")
        temp = period.get("temperature")
        unit = period.get("temperatureUnit")
        short = period.get("shortForecast")
        print(f"{name}: {temp}{unit} - {short}")


def main(argv: Optional[list[str]] = None) -> None:
    """
    Entry point for the CLI. Parses command-line arguments and dispatches to the appropriate command.

    Args:
        argv (Optional[list[str]]): List of command-line arguments. If None, uses sys.argv.
    """
    parser = argparse.ArgumentParser(description="Weather forecast utilities")

    parser.add_argument(
        "-l",
        "--location",
        choices=GRID_POINTS.keys(),
        default="home",
        help="Location to fetch the forecast for",
    )

    sub_cmd = parser.add_subparsers(dest="command")
    sub_cmd.add_parser("update-all", help="Fetch and cache all forecasts")
    sub_cmd.add_parser("show-hourly", help="Display the latest hourly forecast")
    sub_cmd.add_parser("show-daily", help="Display the latest 12h forecast")

    args = parser.parse_args(argv)

    if args.command == "update-all":
        api.update_all_forecasts(args.location.lower())
    elif args.command == "show-hourly":
        data = api.fetch_hourly_forecast(GRID_POINTS[args.location.lower()])
        _print_hourly(data)
    elif args.command == "show-daily":
        data = api.fetch_forecast(GRID_POINTS[args.location.lower()])
        _print_daily(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
