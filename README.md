# Weather Data Utilities

This repository contains a small set of utilities for working with the [National Weather Service](https://weather.gov) (NWS) API.  It includes scripts and Pydantic models for downloading forecast data, caching it locally, and loading it in a typed form.  Command line helpers allow you to fetch and display forecasts for several predefined locations. Use the ``-l``/``--location`` option to select ``home`` (default), ``work``, ``church``, or ``ehhs``.

## Project Layout

```
.
├── utils/
│   ├── api.py       # Functions to fetch and cache forecasts
│   ├── models.py    # Pydantic models describing NWS JSON structures
│   └── __init__.py
├── forecast_notebook.ipynb  # Example notebook
├── map-it.py                # Simple Folium demo to draw a polygon
├── openapi.json             # Official NWS OpenAPI specification
├── pyproject.toml           # Project metadata and dependencies
└── requirements.txt         # Additional pinned dependencies
```

## Usage

The utilities assume Python `3.13+`. Install dependencies from the provided lock file or `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

To update all cached forecasts for a given location, run:

```bash
python main.py -l home update-all
```

You can also display the latest forecasts directly:

```bash
python main.py -l home show-hourly  # hourly forecast
python main.py -l home show-daily   # 12-hour forecast
```

Cached JSON files are written to the `data/` directory with the location name included in the filename (for example, `home_CACHED_FORCAST_DATA.json`). You can explore or further process these files with the models in `utils/models.py`.

The `forecast_notebook.ipynb` notebook demonstrates loading the cached data and validating it using the Pydantic models. It also prints the first forecast period as an example.

The small `map-it.py` script demonstrates drawing a polygon with [Folium](https://python-visualization.github.io/folium/) around Waynesville, NC:

```bash
python map-it.py
```

This produces a `weather_map.html` file that can be opened in a browser.

## License

This repository does not include an explicit license file. Consult the contributors if you wish to use the code.

