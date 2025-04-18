FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y build-essential

# Install poetry
RUN pip install poetry

# Smarter caching. 
# We don't want to get new dependencies on every build unless necessary
COPY scraper/pyproject.toml scraper/poetry.lock /app/
WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
# Copy project files
WORKDIR /app/scraper

COPY scraper/ /app/scraper
# common dependencies are in common
COPY common/ /app/scraper/common

# Entry point
CMD ["python", "scraper.py"]
