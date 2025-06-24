from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from Weather import api, models

app = FastAPI()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
html_dir = PROJECT_ROOT / "static" / "html"


def get_weather_data() -> models.ForecastData | None:
    """
    Fetches weather data from cached NWS API data.
    """
    return api.load_cached_data("work_CACHED_FORECAST_DATA.json")


@app.get("/api/weather")
async def weather_api():
    weatherData = get_weather_data()
    if weatherData is None:
        return {"error": "No weather data available."}
    forecast_data = weatherData.getForecast()
    return {"weatherData": forecast_data}


app.mount("/", StaticFiles(directory=str(html_dir), html=True), name="static")
