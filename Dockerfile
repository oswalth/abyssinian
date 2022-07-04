FROM python:3.10.1-buster
SHELL ["/bin/bash", "-c", "-o", "pipefail"]

LABEL description="Test project for deploying FastAPI app to AWS Lambda"
LABEL maintainer="Vladimir Carpa <oswalth2@gmail.com>"

ENV APP_SYSTEM_PACKAGES="gcc libyaml-dev locales-all"
RUN apt-get update -qq -y \
    && apt-get upgrade -q -y \
    && apt-get install --no-install-recommends -y ${APP_SYSTEM_PACKAGES} \
    && apt-get autoremove -y

ENV APP_HOME="/app"

# Setup application (non-root) user
ENV APP_USER="app"
RUN groupadd -r ${APP_USER} \
    && useradd -r -g ${APP_USER} -d ${APP_HOME} -s /sbin/nologin -c "Application user" -m ${APP_USER}

# Create poetry home directory
ENV POETRY_HOME="/opt/poetry"
RUN mkdir ${POETRY_HOME} && chown ${APP_USER}:${APP_USER} ${POETRY_HOME}

# Change to the project directory & project user
WORKDIR ${APP_HOME}
USER ${APP_USER}:${APP_USER}

ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV PIP_DISABLE_PIP_VERSION_CHECK="on"
ENV PYTHONUNBUFFERED="1"

ENV POETRY_VERSION="1.1.13"
# Instead of using `get-poetry.py` or `install-poetry.py` script from
# https://python-poetry.org/docs/#installation, install poetry by creating
# `venv` and installing expected poetry version there
RUN python3 -m venv ${POETRY_HOME} \
    && ${POETRY_HOME}/bin/pip install --upgrade pip \
    && ${POETRY_HOME}/bin/pip install --no-cache-dir poetry==${POETRY_VERSION}

# Install project dependencies
COPY ./pyproject.toml ./
COPY ./poetry.toml ./
COPY ./poetry.lock ./


# First, install main project dependencies
RUN poetry install --no-dev --no-root

COPY ./src ./src
COPY ./alembic.ini ./
COPY ./alembic ./alembic

ENV PYTHONPATH="${PYTHONPATH}:${APP_HOME}/src"

# Setup entrypoint and make it executable
COPY ./entrypoint.sh .
USER root
RUN chmod +x ./entrypoint.sh

USER ${APP_USER}:${APP_USER}