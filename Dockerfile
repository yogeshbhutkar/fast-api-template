FROM python:3.12-slim

# Install system dependencies for asyncpg.
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install asyncpg

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Expose the application port.
EXPOSE 8000

# Run the application.
CMD ["uv", "run", "-m", "src.main"]
