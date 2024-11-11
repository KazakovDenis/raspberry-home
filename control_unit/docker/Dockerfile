FROM python:3.9-slim as base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && \
    apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY poetry.lock pyproject.toml docker/entrypoint.sh /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev --remove-untracked

FROM base
WORKDIR /app
COPY bot/ /app/bot/
ENTRYPOINT ["./entrypoint.sh"]
