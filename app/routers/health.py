# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: Health Check Router
# File: app/routers/health.py
# ----------------------------------------------------------
# Description:
# Minimal health endpoint used by Docker, CI/CD, and
# external service monitors. Returns a simple JSON
# response confirming the API is running.
# ----------------------------------------------------------

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}
