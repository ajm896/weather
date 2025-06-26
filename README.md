# Weather Data Utilities

This repository provides a small weather application built on top of the
[National Weather Service](https://weather.gov) (NWS) API.  It includes Python
utilities for downloading and caching forecasts, a FastAPI based web service and
a simple HTML/JavaScript frontend.  Command line helpers allow you to fetch and
display forecasts for several predefined locations. Use the ``-l``/``--location``
option to select ``home`` (default), ``work``, ``church`` or ``ehhs``.

## Project Layout

```
.
├── src/
│   ├── Cli/                 # Command line interface module
│   ├── WebApp/              # FastAPI application
│   └── weather/             # API helpers and Pydantic models
├── static/                  # Front-end HTML/JS assets
├── conf/                    # Configuration for the Caddy web server
├── docker-compose.yml       # Compose file with Traefik and Caddy
├── Dockerfile               # Container image definition
├── openapi.json             # Official NWS OpenAPI specification
├── pyproject.toml           # Project metadata and dependencies
└── requirements.txt         # Additional pinned dependencies
```

## Usage

The project targets Python `3.13+`. Install dependencies using the
[uv](https://github.com/astral-sh/uv) package manager from the provided lock file
or `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

### Command line interface

Update cached forecasts for a location:

```bash
python -m Cli.main -l home update-all
```

Display the most recent hourly or 12h forecast:

```bash
python -m Cli.main -l home show-hourly
python -m Cli.main -l home show-daily
```

Cached JSON files are written to the ``data/`` directory with the location name
included in the filename (for example,
``home_CACHED_FORECAST_DATA.json``).  The models in ``src/weather/models.py`` can
be used to further process these files.

### Web application

The FastAPI service exposes two endpoints:

``/v1/api/weather/{location}`` – return the latest cached forecast

``/v1/api/weather/{location}/update`` – refresh the cache for a location.

For development you can start the server directly:

```bash
uvicorn src.WebApp.app:app --reload
```

The ``static/`` directory contains a small front‑end (``index.html`` and
``script.js``) that consumes these endpoints.

### Docker

The project includes a ``Dockerfile`` and ``docker-compose.yml`` that run the
FastAPI backend behind Traefik and serve the front‑end via Caddy. Build and run
everything with:

```bash
docker compose up --build
```

The `forecast_notebook.ipynb` notebook demonstrates loading the cached data and validating it using the Pydantic models. It also prints the first forecast period as an example.

The small `map-it.py` script demonstrates drawing a polygon with [Folium](https://python-visualization.github.io/folium/) around Waynesville, NC:

```bash
python map-it.py
```

This produces a `weather_map.html` file that can be opened in a browser.

## Code Overview

The Python packages live in the `src/` directory:

- `src/weather/` – helper functions and Pydantic models for interacting with
  the NWS API.
- `src/Cli/` – the command line interface implemented in `main.py`.
- `src/WebApp/` – the FastAPI application with two weather endpoints.

Each module and function is documented with inline docstrings following PEP 8.

## License

This repository does not include an explicit license file. Consult the contributors if you wish to use the code.

