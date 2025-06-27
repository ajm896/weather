"""
models.py

Data models for weather forecast and gridpoint data, using Pydantic for
validation and serialization.

This module defines a set of Pydantic models representing the structure of
weather forecast data as returned by the National Weather Service (NWS) API and
similar sources. The models cover both 12-hour and hourly forecast periods,
quantitative value layers and GeoJSON features for spatial data. These models
are used for parsing, validating and working with weather data in a structured
way throughout the application.

Classes:
    _QuantitativeValue – value with units (e.g., temperature, elevation)
    _Gridpoint12hForecastPeriod – a single 12-hour forecast period
    _GeoJsonGeometry – the geometry section of a GeoJSON feature
    _Gridpoint12hForecast – a 12-hour forecast for a gridpoint
    _GridpointHourlyForecastPeriod – a single hourly forecast period
    _GridpointHourlyForecast – an hourly forecast for a gridpoint
    _GridpointQuantitativeValueLayer – a layer of quantitative values for a
        gridpoint (e.g., temperature, humidity)
    _Gridpoint – raw forecast data for a 2.5km grid square
    GridpointGeoJson – a GeoJSON feature for gridpoint data
    Gridpoint12hForecastGeoJson – a GeoJSON feature for 12-hour data
    GridpointHourlyForecastGeoJson – a GeoJSON feature for hourly data
"""

from datetime import datetime
from pydantic import BaseModel, Discriminator, Field
from typing import Annotated, Any, Union, Literal


class _QuantitativeValue(BaseModel):
    """
    Represents a quantitative value with units, such as temperature,
    elevation or probability of precipitation.

    Attributes:
        value (int | float): The numeric value.
        unitCode (str): The unit of measurement (e.g., 'wmoUnit:degC',
            'wmoUnit:percent').
    """

    value: int | float
    unitCode: str

    def __str__(self) -> str:
        """Return a friendly representation like ``"{value} {unit}"``."""
        return f"{self.value} {self.unitCode}"


class _Gridpoint12hForecastPeriod(BaseModel):
    """
    Represents a single 12-hour forecast period, including temperature,
    precipitation, wind and forecast text.

    Attributes:
        number (int): Sequence number of the period.
        name (str): Name of the period (e.g., 'Tonight', 'Monday').
        startTime (str): ISO8601 start time.
        endTime (str): ISO8601 end time.
        isDaytime (bool): True if the period is during the day.
        temperature (int | None): Temperature value.
        temperatureUnit (str | None): Unit of temperature.
        temperatureTrend (str | None): Trend of temperature (e.g., 'rising').
        probabilityOfPrecipitation (_QuantitativeValue | None):
            Probability of precipitation.
        windSpeed (str | None): Wind speed as a string (e.g., '5 to 10 mph').
        windDirection (str | None): Wind direction (e.g., 'NW').
        icon (str | None): URL to an icon representing the forecast.
        shortForecast (str | None): Short text summary.
        detailedForecast (str | None): Detailed text summary.
    """

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
        """Return ``"{name}: {forecast}"`` for quick display."""
        forecast = (
            self.detailedForecast or self.shortForecast or ("No forecast available")
        )
        return f"{self.name}: {forecast}"


class _GeoJsonGeometry(BaseModel):
    """
    Represents the geometry section of a GeoJSON feature, typically a
    polygon or multipolygon.

    Attributes:
        type (str): The geometry type (e.g., 'Polygon').
        coordinates (list[list[list[float]]]): Coordinates of the geometry.
    """

    type: str
    coordinates: list[list[list[float]]]

    def __str__(self) -> str:
        """Return a readable summary of the geometry."""
        return f"Geometry:\ntype: {self.type}\n\nCoordinates:\n{self.coordinates})"


class _Gridpoint12hForecast(BaseModel):
    """
    Represents a 12-hour forecast for a gridpoint, including metadata and a
    list of forecast periods.

    Attributes:
        units (str): Units of measurement.
        forecastGenerator (str): Source of the forecast.
        generatedAt (str): ISO8601 timestamp when generated.
        updateTime (str): ISO8601 timestamp of last update.
        validTimes (str): Valid time range for the forecast.
        elevation (_QuantitativeValue): Elevation of the gridpoint.
        periods (list[_Gridpoint12hForecastPeriod]): List of forecast periods.
    """

    type: Literal["12h"] = "12h"
    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: _QuantitativeValue
    periods: list[_Gridpoint12hForecastPeriod]

    def __str__(self) -> str:
        """Return a detailed multiline description of the forecast."""
        return f"""
Gridpoint 12h Forecast:
Units: {self.units}
ForecastGenerator: {self.forecastGenerator}
GeneratedAt: {self.generatedAt}
UpdateTime: {self.updateTime}
ValidTimes: {self.validTimes}
Elevation: {self.elevation}

Periods:
{"\n\n".join(str(period) for period in self.periods)}
        """


class _GridpointHourlyForecastPeriod(BaseModel):
    """
    Represents a single hourly forecast period including temperature,
    precipitation, wind and forecast text.

    Attributes:
        number (int): Sequence number of the period.
        name (str): Name of the period (e.g., '1am').
        startTime (str): ISO8601 start time.
        endTime (str): ISO8601 end time.
        isDaytime (bool): True if the period is during the day.
        temperature (int | None): Temperature value.
        temperatureUnit (str | None): Unit of temperature.
        temperatureTrend (str | None): Trend of temperature.
        probabilityOfPrecipitation (_QuantitativeValue | None):
            Probability of precipitation.
        windSpeed (str | None): Wind speed as a string.
        windDirection (str | None): Wind direction.
        icon (str | None): URL to an icon representing the forecast.
        shortForecast (str | None): Short text summary.
        detailedForecast (str | None): Detailed text summary.
    """

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
        """Return the start time and brief forecast for one hour."""
        starttime = datetime.fromisoformat(self.startTime)
        summary = (
            self.detailedForecast or self.shortForecast or ("No forecast available")
        )
        return f"{starttime.ctime()}: {summary}"


class _GridpointHourlyForecast(BaseModel):
    """
    Represents an hourly forecast for a gridpoint, including metadata and a
    list of hourly forecast periods.

    Attributes:
        units (str): Units of measurement.
        forecastGenerator (str): Source of the forecast.
        generatedAt (str): ISO8601 timestamp when generated.
        updateTime (str): ISO8601 timestamp of last update.
        validTimes (str): Valid time range for the forecast.
        elevation (_QuantitativeValue): Elevation of the gridpoint.
        periods (list[_GridpointHourlyForecastPeriod]):
            List of hourly forecast periods.
    """

    units: str
    forecastGenerator: str
    generatedAt: str
    updateTime: str
    validTimes: str
    elevation: _QuantitativeValue
    periods: list[_GridpointHourlyForecastPeriod]

    def __str__(self) -> str:
        """Return a multiline representation of the hourly forecast."""
        return f"""
Gridpoint Hourly Forecast:
Units: {self.units}
ForecastGenerator: {self.forecastGenerator}
GeneratedAt: {self.generatedAt}
UpdateTime: {self.updateTime}
ValidTimes: {self.validTimes}
Elevation: {self.elevation}

Periods:
{"\n\n".join(str(period) for period in self.periods)}
"""


class _GridpointQuantitativeValue(BaseModel):
    validTime: str
    value: Any

    def __str__(self) -> str:
        """Return ``"{timestamp} --> {value}"``."""
        return f"{self.validTime} --> {self.value}"


class _GridpointQuantitativeValueLayer(BaseModel):
    """
    Represents a layer of quantitative value data for a gridpoint, such as
    temperature or humidity.

    Attributes:
        uom (str): Unit of measurement for the layer.
        values (list[dict[str, int | float | str]]):
            List of value dictionaries for the layer.
    """

    uom: str
    values: list[_GridpointQuantitativeValue]

    def __str__(self) -> str:
        """Return a line-per-value listing of the layer contents."""
        values = ",\n".join(str(value) for value in self.values)
        return f"{self.uom.split(':')[1]}: \n{values}"


class _Gridpoint(BaseModel):
    """
    Represents raw forecast data for a 2.5km grid square, including many
    possible weather data layers.

    Attributes:
        updateTime (str): ISO8601 timestamp of last update.
        validTimes (str): Valid time range for the forecast.
        elevation (_QuantitativeValue): Elevation of the gridpoint.
        forecastOffice (str): Forecast office identifier.
        gridId (str): Grid identifier.
        gridX (int): X coordinate of the gridpoint.
        gridY (int): Y coordinate of the gridpoint.
        temperature (_GridpointQuantitativeValueLayer | None):
            Temperature data layer.
        dewpoint (_GridpointQuantitativeValueLayer | None):
            Dewpoint data layer.
        maxTemperature (_GridpointQuantitativeValueLayer | None):
            Max temperature data layer.
        minTemperature (_GridpointQuantitativeValueLayer | None):
            Min temperature data layer.
        relativeHumidity (_GridpointQuantitativeValueLayer | None):
            Relative humidity data layer.
        apparentTemperature (_GridpointQuantitativeValueLayer | None):
            Apparent temperature data layer.
        # Additional layers may be present as described in the class docstring.
    """

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

    def __str__(self) -> str:
        """Return a multiline summary of the gridpoint's weather data."""
        return """
Gridpoint:
updateTime: {self.updateTime}
validTimes: {self.validTimes}

elevation: {self.elevation}

forecastOffice: {self.forecastOffice}
gridId: {self.gridId}

gridX: {self.gridX}
gridY: {self.gridY}

temperature: {self.temperature}

dewpoint: {self.dewpoint}

maxTemperature: {self.maxTemperature}

minTemperature: {self.minTemperature}

relativeHumidity: {self.relativeHumidity}

apparentTemperature: {self.apparentTemperature}
        """.format(self=self)


class GridpointGeoJson(BaseModel):
    """
    Represents a GeoJSON feature for gridpoint data, including geometry
    and properties.

    Attributes:
        geometry (_GeoJsonGeometry): The geometry of the feature.
        properties (_Gridpoint): The properties (weather data) of the feature.
        type (str): The GeoJSON feature type (usually 'Feature').
    """

    geometry: _GeoJsonGeometry
    properties: _Gridpoint

    kind: Literal["gridpoint"] = Field(default="gridpoint")

    def __str__(self) -> str:
        """Return geometry followed by properties."""
        return f"{self.geometry}\n{self.properties})"


class Gridpoint12hForecastGeoJson(BaseModel):
    """
    Represents a GeoJSON feature for 12-hour forecast data.

    Attributes:
        geometry (_GeoJsonGeometry): The geometry of the feature.
        properties (_Gridpoint12hForecast): The 12-hour forecast properties.
        type (str): The GeoJSON feature type.
    """

    geometry: _GeoJsonGeometry
    properties: _Gridpoint12hForecast
    kind: Literal["12h"] = Field(default="12h")

    def __str__(self) -> str:
        """Return geometry and forecast details separated by a blank line."""
        return f"{self.geometry}\n\n{self.properties})"


class GridpointHourlyForecastGeoJson(BaseModel):
    """
    Represents a GeoJSON feature for hourly forecast data.

    Attributes:
        geometry (_GeoJsonGeometry): The geometry of the feature.
        properties (_GridpointHourlyForecast): The hourly forecast properties.
        type (str): The GeoJSON feature type.
    """

    geometry: _GeoJsonGeometry
    properties: _GridpointHourlyForecast
    kind: Literal["hourly"] = Field(default="hourly")

    def __str__(self) -> str:
        """Return geometry and hourly forecast details separated by a
        blank line."""
        return f"{self.geometry}\n\n{self.properties})"


class ForecastData(BaseModel):
    kind: Literal["gridpoint", "12h", "hourly"]
    data: Annotated[
        Union[
            GridpointGeoJson,
            Gridpoint12hForecastGeoJson,
            GridpointHourlyForecastGeoJson,
        ],
        Discriminator("kind"),
    ]

    def getForecast(self) -> dict[str, Any]:
        """
        Returns the forecast data as a dictionary.
        This is useful for serialization or further processing.
        """
        return self.data.properties.model_dump()

    def __str__(self):
        return f"{self.kind}: {self.data}"
