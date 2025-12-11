# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12/13: FastAPI Modular Calculator + JWT Auth
# File: Dockerfile
# ----------------------------------------------------------
# Description:
# Production-ready Dockerfile for running the FastAPI Modular
# Calculator inside Docker. Includes:
#   • Python 3.12-slim base
#   • PostgreSQL client for pg_isready checks
#   • Non-root appuser for security
#   • layer-cached dependency installation
#   • Healthcheck hitting /health
#   • Uvicorn (2 workers) for performance
# ----------------------------------------------------------


# ----------------------------------------------------------
# 1. Base Image
# ----------------------------------------------------------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app


# ----------------------------------------------------------
# 2. Install System Dependencies
# ----------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
        curl \
        # ------------------------------------------------------
        # Assignment 13 Update:
        # Install Node.js + npm for Playwright dependencies
        # (Required when GitHub Actions builds the Docker image)
        # ------------------------------------------------------
        nodejs npm \
    && rm -rf /var/lib/apt/lists/*


# ----------------------------------------------------------
# 3. Security: Create Non-root Application User
# ----------------------------------------------------------
RUN groupadd -r appgroup && useradd -r -g appgroup appuser


# ----------------------------------------------------------
# 4. Install Python Dependencies
# ----------------------------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt


# ----------------------------------------------------------
# 5. Copy Application Source Code
# ----------------------------------------------------------
COPY . /app


# ----------------------------------------------------------
# 6. Set Permissions
# ----------------------------------------------------------
RUN chown -R appuser:appgroup /app
USER appuser


# ----------------------------------------------------------
# 7. Expose Application Port & Healthcheck
# ----------------------------------------------------------
EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1


# ----------------------------------------------------------
# 8. Start FastAPI using Uvicorn
# ----------------------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
