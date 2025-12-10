# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: FastAPI JWT Authentication + UI
# File: Dockerfile
# ----------------------------------------------------------
# Description:
# Production Dockerfile for FastAPI (JWT Auth + UI Pages).
# Includes:
#   • Python 3.12-slim base
#   • Layer caching for faster rebuilds
#   • Non-root container user
#   • Postgres client for optional DB readiness
#   • Healthcheck pointing to /health
#   • Runs Uvicorn with 2 workers
# ----------------------------------------------------------


# ----------------------------------------------------------
# 1. Base Image
# ----------------------------------------------------------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/appuser/.local/bin:$PATH" \
    DATABASE_URL="sqlite:///./app.db" \
    UVICORN_PORT=8000

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
    && rm -rf /var/lib/apt/lists/*


# ----------------------------------------------------------
# 3. Add Non-root User
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
# 6. Set Proper File Ownership
# ----------------------------------------------------------
RUN chown -R appuser:appgroup /app
USER appuser


# ----------------------------------------------------------
# 7. Expose Port + Healthcheck
# ----------------------------------------------------------
EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:${UVICORN_PORT}/health || exit 1


# ----------------------------------------------------------
# 8. Start FastAPI with Uvicorn
# ----------------------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
