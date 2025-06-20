from pydantic import BaseModel

class QuantitativeValue(BaseModel):
    """Probability of precipitation."""
    value: int | float
    unitCode: str

    def __str__(self) -> str:
        return f"{self.value} {self.unitCode}"

class Gridpoint12hForecastPeriod(BaseModel):
    """A single forecast period."""
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int | None = None
    temperatureUnit: str | None = None
    temperatureTrend: str | None = None
    probabilityOfPrecipitation: QuantitativeValue | None = None
    windSpeed: str | None = None
    windDirection: str | None = None
    icon: str | None = None
    shortForecast: str | None = None
    detailedForecast: str | None = None

    def __str__(self) -> str:
        return f"{self.name} ({self.startTime} - {self.endTime}): {self.shortForecast or self.detailedForecast or 'No forecast available'}"

class GeoJsonGeometry(BaseModel):
    type: str
    coordinates: list[list[list[float]]]

class Gridpoint12hForecast(BaseModel):
    """A 12-hour forecast for a gridpoint."""
    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: QuantitativeValue
    periods: list[Gridpoint12hForecastPeriod]

class Gridpoint12hForecastGeoJson(BaseModel):
    """A GeoJSON feature. Please refer to 
    IETF RFC 7946 for information on the GeoJSON format.
    """
    geometry: GeoJsonGeometry
    properties: Gridpoint12hForecast
    type: str

class GridpointHourlyForecastPeriod(BaseModel):
    """A single hourly forecast period."""
    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int | None = None
    temperatureUnit: str | None = None
    temperatureTrend: str | None = None
    probabilityOfPrecipitation: QuantitativeValue | None = None
    windSpeed: str | None = None
    windDirection: str | None = None
    icon: str | None = None
    shortForecast: str | None = None
    detailedForecast: str | None = None

class GridpointHourlyForecast(BaseModel):
    """An hourly forecast for a gridpoint."""
    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: QuantitativeValue
    periods: list[GridpointHourlyForecastPeriod]

class GridpointHourlyForecastGeoJson(BaseModel):
    """A GeoJSON feature for hourly forecast data."""
    geometry: GeoJsonGeometry
    properties: GridpointHourlyForecast
    type: str