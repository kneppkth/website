# syntax=docker/dockerfile:experimental
######################################
# Builder step #######################
######################################
FROM python:3.10.2-slim-bullseye AS builder

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Use Python binaries from venv
ENV PATH="/backend/venv/bin:$PATH"

# Pinned versions
ENV PIP_PIP_VERSION 21.2.4

# Setup the virtualenv
RUN python -m venv /backend/venv
WORKDIR /backend

# Install dependencies
COPY ./requirements.txt .
RUN set -x && \
    pip install pip==$PIP_PIP_VERSION && \
    pip install -r requirements.txt && \
    pip check

######################################
# Runtime step #######################
######################################
FROM python:3.10.2-slim-bullseye AS runtime

# Extra Python environment variables
ENV XDG_CACHE_HOME /tmp/pip/.cache
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Use Python binaries from venv
ENV PATH="/backend/venv/bin:$PATH"

# Pinned versions
ENV APT_GETTEXT_VERSION 0.21-*
ENV APT_MAKE_VERSION 4.3-*
ENV APT_WAIT_FOR_IT_VERSION 0.0~git20180723-1
ENV APT_MIME_SUPPORT 3.*
ENV APT_LIB_MAGIC_DEV 1:5.39-*

# Django settings
ENV DJANGO_SETTINGS_MODULE knepp.settings
ENV DJANGO_STATIC_ROOT /backend/static

# Setup app user and directory
RUN set -x && groupadd -g 8000 backend && useradd -r -u 8000 -g backend backend -d /backend && \
    mkdir -p /backend/internal_media && chown -R backend:backend /backend

# Install system dependencies
# SC2215 is ignored due to https://github.com/hadolint/hadolint/issues/347
# hadolint ignore=SC2215
RUN set -x && apt-get update && apt-get install --no-install-recommends -y \
    gettext=$APT_GETTEXT_VERSION \
    make=$APT_MAKE_VERSION \
    wait-for-it=$APT_WAIT_FOR_IT_VERSION \
    mime-support=$APT_MIME_SUPPORT \
    libmagic-dev=$APT_LIB_MAGIC_DEV

RUN mkdir /data && chown -R backend:backend /data

# Install source code
USER backend
COPY --chown=backend Makefile ./
COPY --from=builder /backend/venv backend/venv
COPY --chown=backend backend backend
WORKDIR /backend

# Collect static files
RUN set -x && \
    DJANGO_SECRET_KEY=none python manage.py compilemessages --locale sv && \
    DJANGO_SECRET_KEY=none python manage.py collectstatic --no-input

# Set port
EXPOSE 8000
