from pydantic import BaseModel


class _QuantitativeValue(BaseModel):
    """Probability of precipitation."""

    value: int | float
    unitCode: str

    def __str__(self) -> str:
        return f"{self.value} {self.unitCode}"


class _Gridpoint12hForecastPeriod(BaseModel):
    """A single forecast period."""

    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int | None = None
    temperatureUnit: str | None = None
    temperatureTrend: str | None = None
    probabilityOfPrecipitation: _QuantitativeValue | None = None
    windSpeed: str | None = None
    windDirection: str | None = None
    icon: str | None = None
    shortForecast: str | None = None
    detailedForecast: str | None = None

    def __str__(self) -> str:
        return f"{self.name} ({self.startTime} - {self.endTime}): {self.shortForecast or self.detailedForecast or 'No forecast available'}"


class _GeoJsonGeometry(BaseModel):
    type: str
    coordinates: list[list[list[float]]]


class _Gridpoint12hForecast(BaseModel):
    """A 12-hour forecast for a gridpoint."""

    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: _QuantitativeValue
    periods: list[_Gridpoint12hForecastPeriod]


class _GridpointHourlyForecastPeriod(BaseModel):
    """A single hourly forecast period."""

    number: int
    name: str
    startTime: str
    endTime: str
    isDaytime: bool
    temperature: int | None = None
    temperatureUnit: str | None = None
    temperatureTrend: str | None = None
    probabilityOfPrecipitation: _QuantitativeValue | None = None
    windSpeed: str | None = None
    windDirection: str | None = None
    icon: str | None = None
    shortForecast: str | None = None
    detailedForecast: str | None = None


class _GridpointHourlyForecast(BaseModel):
    """An hourly forecast for a gridpoint."""

    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: _QuantitativeValue
    periods: list[_GridpointHourlyForecastPeriod]


class _GridpointQuantitativeValueLayer(BaseModel):
    """A layer of quantitative value data for a gridpoint."""

    uom: str
    values: list[dict[str, int | float | str]]

    def __str__(self) -> str:
        return f"{self.values} {self.uom}"


class _Gridpoint(BaseModel):
    """
    Raw forecast data for a 2.5km grid square.
    This is a list of all potential data layers that may appear.
    Some layers may not be present in all areas.

    temperature
    dewpoint
    maxTemperature
    minTemperature
    relativeHumidity
    apparentTemperature
    heatIndex
    windChill
    wetBulbGlobeTemperature
    skyCover
    windDirection
    windSpeed
    windGust
    weather
    hazards: Watch and advisory products in effect
    probabilityOfPrecipitation
    quantitativePrecipitation
    iceAccumulation
    snowfallAmount
    snowLevel
    ceilingHeight
    visibility
    transportWindSpeed
    transportWindDirection
    mixingHeight
    hainesIndex
    lightningActivityLevel
    twentyFootWindSpeed
    twentyFootWindDirection
    waveHeight
    wavePeriod
    waveDirection
    primarySwellHeight
    primarySwellDirection
    secondarySwellHeight
    secondarySwellDirection
    wavePeriod2
    windWaveHeight
    dispersionIndex
    pressure: Barometric pressure
    probabilityOfTropicalStormWinds
    probabilityOfHurricaneWinds
    potentialOf15mphWinds
    potentialOf25mphWinds
    potentialOf35mphWinds
    potentialOf45mphWinds
    potentialOf20mphWindGusts
    potentialOf30mphWindGusts
    potentialOf40mphWindGusts
    potentialOf50mphWindGusts
    potentialOf60mphWindGusts
    grasslandFireDangerIndex
    probabilityOfThunder
    davisStabilityIndex
    atmosphericDispersionIndex
    lowVisibilityOccurrenceRiskIndex
    stability
    redFlagThreatIndex"""

    updateTime: str
    validTimes: str
    elevation: _QuantitativeValue
    forecastOffice: str
    gridId: str
    gridX: int
    gridY: int
    temperature: _GridpointQuantitativeValueLayer | None = None
    dewpoint: _GridpointQuantitativeValueLayer | None = None
    maxTemperature: _GridpointQuantitativeValueLayer | None = None
    minTemperature: _GridpointQuantitativeValueLayer | None = None
    relativeHumidity: _GridpointQuantitativeValueLayer | None = None
    apparentTemperature: _GridpointQuantitativeValueLayer | None = None


class GridpointGeoJson(BaseModel):
    """A GeoJSON feature for gridpoint data."""

    geometry: _GeoJsonGeometry
    properties: _Gridpoint

    type: str

    def __str__(self) -> str:
        return f"GridpointGeoJson(type={self.type}, properties={self.properties})"


class Gridpoint12hForecastGeoJson(BaseModel):
    """A GeoJSON feature. Please refer to
    IETF RFC 7946 for information on the GeoJSON format.
    """

    geometry: _GeoJsonGeometry
    properties: _Gridpoint12hForecast
    type: str


class GridpointHourlyForecastGeoJson(BaseModel):
    """A GeoJSON feature for hourly forecast data."""

    geometry: _GeoJsonGeometry
    properties: _GridpointHourlyForecast
    type: str
