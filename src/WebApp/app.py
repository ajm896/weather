from fastapi import FastAPI

from Weather import api, models

app = FastAPI()


def get_weather_data() -> models.ForecastData | None:
    """
    Fetches weather data from cached NWS API data.
    """
    return api.load_cached_data("work_CACHED_FORCAST_DATA.json")


@app.get("/")
async def read_root():
    weatherData = get_weather_data()
    if weatherData is None:
        return {"error": "No weather data available."}
    forecast_data = weatherData.getForecast()
    return {"weatherData": forecast_data}
