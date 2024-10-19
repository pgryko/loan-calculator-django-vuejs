# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy project
COPY . /app/

# Run migrations and collect static files
RUN poetry run python manage.py migrate
RUN poetry run python manage.py collectstatic --noinput

# Run the application
CMD ["poetry", "run", "uvicorn", "loan_calculator.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
