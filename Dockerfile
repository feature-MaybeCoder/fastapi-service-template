FROM python:3.10-slim
LABEL authors="lastdarknes"

# Define workdir
COPY . /build
WORKDIR /build

# Update system
RUN apt-get -y update
RUN apt-get -y install curl

# Install Poetry
RUN curl -sSL \
    https://install.python-poetry.org | \
    POETRY_HOME=/opt/poetry python3  && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install dependencies
COPY poetry.lock pyproject.toml /build/
RUN poetry install --no-interaction --no-ansi  --no-root

# Run app
ENTRYPOINT uvicorn app.main:fa_app --reload --host 0.0.0.0 --port 8010
