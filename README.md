# Weather Data Utilities

This repository contains a small set of utilities for working with the [National Weather Service](https://weather.gov) (NWS) API. It includes scripts and Pydantic models for downloading forecast data, caching it locally, and loading it in a typed form.

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

To update all cached forecasts, run:

```bash
python -c "import utils.api as api; api.update_all_forecasts()"
```

Cached JSON files (`cached_forecast_data.json`, `cached_hourly_data.json`, and `cached_raw_data.json`) will be written in the repository root. You can explore or further process these files with the models in `utils/models.py`.

The `forecast_notebook.ipynb` notebook demonstrates loading the cached data and validating it using the Pydantic models. It also prints the first forecast period as an example.

The small `map-it.py` script shows how to draw a polygon with [Folium](https://python-visualization.github.io/folium/) around Waynesville, NC:

```bash
python map-it.py
```

This produces an `waynesville_polygon_map.html` file that can be opened in a browser.

## License

This repository does not include an explicit license file. Consult the contributors if you wish to use the code.

