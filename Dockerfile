FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

RUN playwright install --with-deps

COPY . .

