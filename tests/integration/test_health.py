# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Health Endpoint Test
# File: tests/unit/test_health.py
# ----------------------------------------------------------
# Description:
# Verifies the /health endpoint responds correctly and that
# the router is mounted and functional without requiring any
# authentication or database connection. Ensures predictable
# JSON output and correct HTTP status codes using TestClient.
# ----------------------------------------------------------

from fastapi.testclient import TestClient
from main import app


def test_health_endpoint():
    """Ensure /health returns expected success response."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
