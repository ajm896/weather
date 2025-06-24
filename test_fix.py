#!/usr/bin/env python3

# Quick test to verify the fix works
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from Weather import api


# Test loading cached data
def test_load_cached_data():
    print("Testing load_cached_data function...")

    # Test with 12h forecast data
    weather_data = api.load_cached_data("work_CACHED_FORCAST_DATA.json")

    if weather_data is None:
        print("ERROR: No weather data loaded")
        return False

    print(f"Loaded weather data type: {type(weather_data)}")
    print(f"Weather data forecast type: {weather_data.type}")

    # Test if we can call getForecast() method
    try:
        forecast_data = weather_data.getForecast()
        print(f"getForecast() returned: {type(forecast_data)}")
        print(f"Number of periods: {len(forecast_data.get('periods', []))}")
        return True
    except Exception as e:
        print(f"ERROR calling getForecast(): {e}")
        return False


if __name__ == "__main__":
    success = test_load_cached_data()
    if success:
        print("✅ Fix verified - the weather data now works correctly!")
    else:
        print("❌ Fix failed - there are still issues")
