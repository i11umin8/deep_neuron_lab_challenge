FROM python:3.13-slim

# System deps
RUN apt-get update && apt-get install -y build-essential

# Install poetry
RUN pip install poetry

# Smarter caching. 
# We don't want to get new dependencies on every build unless necessary
COPY api/pyproject.toml api/poetry.lock /app/
WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
# Copy project files
WORKDIR /app/api

COPY api/ /app/api
# common dependencies are in common
COPY common/ /app/api/common
