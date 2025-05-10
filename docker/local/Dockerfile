# Dockerfile
FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PYTHONPATH=/app


WORKDIR /app

COPY . .

RUN rm -rf /app/.venv
RUN rm -rf /app/app
RUN rm -rf /app/migrations


RUN poetry install --no-root