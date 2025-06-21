"""Command line interface for the weather utilities."""

from __future__ import annotations

import argparse
from typing import Optional

from utils import api


def _print_hourly(data: dict) -> None:
    """Print a simple summary of hourly forecast data."""
    periods = data.get("properties", {}).get("periods", [])
    for period in periods:
        temp = period.get("temperature")
        unit = period.get("temperatureUnit")
        short = period.get("shortForecast")
        start = period.get("startTime")
        print(f"{start}: {temp}{unit} - {short}")


def _print_daily(data: dict) -> None:
    """Print a simple summary of 12 hour forecast data."""
    periods = data.get("properties", {}).get("periods", [])
    for period in periods:
        name = period.get("name")
        temp = period.get("temperature")
        unit = period.get("temperatureUnit")
        short = period.get("shortForecast")
        print(f"{name}: {temp}{unit} - {short}")


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Weather forecast utilities")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("update-all", help="Fetch and cache all forecasts")
    sub.add_parser("show-hourly", help="Display the latest hourly forecast")
    sub.add_parser("show-daily", help="Display the latest 12h forecast")

    args = parser.parse_args(argv)

    if args.command == "update-all":
        api.update_all_forecasts()
    elif args.command == "show-hourly":
        data = api.fetch_hourly_forecast()
        _print_hourly(data)
    elif args.command == "show-daily":
        data = api.fetch_forecast()
        _print_daily(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

