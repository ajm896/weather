from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from weather import api, models

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://weather.localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_weather_data(location: str) -> models.ForecastData | None:
    """
    Fetches weather data from cached NWS API data.
    """
    return api.load_cached_data(f"{location}_CACHED_FORECAST_DATA.json")


@app.get("/v1/api/weather/{location}")
async def weather_api(location: str):
    weatherData = get_weather_data(location)
    if weatherData is None:
        return {"error": "No weather data available."}
    forecast_data = weatherData.getForecast()
    return {"weatherData": forecast_data}


@app.get("/v1/api/weather/{location}/update")
async def update_weather_api(location: str):
    """
    Updates the weather data for a given location.
    """
    api.update_all_forecasts(location=location)
    return {"message": "Weather data updated successfully."}
