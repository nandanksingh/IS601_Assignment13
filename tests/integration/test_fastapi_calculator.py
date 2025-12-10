# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: FastAPI Calculator Tests
# File: tests/integration/test_fastapi_calculator.py
# ----------------------------------------------------------
# Description:
# Simple end-to-end calculator functionality test.
# Creates a user → logs in → performs a basic operation.
# Ensures HTTP 201 and correct calculation results.
# ----------------------------------------------------------

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_basic_add_operation():
    # Register user
    client.post(
        "/auth/register",
        json={
            "first_name": "Calc",
            "last_name": "User",
            "username": "calc_user",
            "email": "calc@example.com",
            "password": "Pass123",
            "confirm_password": "Pass123",
            "mobile": "1234567890"
        },
    )

    # Login and retrieve token (Assignment-13 uses identifier)
    token = client.post(
        "/auth/login",
        json={"identifier": "calc_user", "password": "Pass123"},
    ).json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create calculation
    response = client.post(
        "/calculations",
        json={"type": "add", "a": 4, "b": 6},
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["result"] == 10
    assert data["a"] == 4
    assert data["b"] == 6
    assert data["type"].lower() == "add"
