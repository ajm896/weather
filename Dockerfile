FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Copy the project into the image
ADD . /weather

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /weather
RUN uv sync --locked
ENV PATH="/weather/.venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "src.webapp.app:app", "--host", "0.0.0.0", "--port", "8000"]