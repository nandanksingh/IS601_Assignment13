# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: Calculation Route Tests
# File: tests/integration/test_calculations.py
# ----------------------------------------------------------
# Description:
# Test suite validating BREAD operations for the calculations
# API. Covers create, list, read, update, and delete actions.
# Requires a valid authenticated user and exercises both
# normal operation and error-handling paths such as division
# by zero to ensure consistent backend behavior.
# ----------------------------------------------------------

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ----------------------------------------------------------
# Helper: Register + Login for token
# ----------------------------------------------------------
def auth_register():
    """Register a valid test user for calculation tests."""
    client.post(
        "/auth/register",
        json={
            "first_name": "Calc",
            "last_name": "User",
            "username": "calc_user",
            "email": "calc@ex.com",
            "mobile": "9998887777",
            "password": "Pass123A",
            "confirm_password": "Pass123A",
        },
    )


def auth_token():
    """Return access_token after registration + login."""
    auth_register()
    res = client.post(
        "/auth/login",
        json={
            "identifier": "calc@ex.com",   # email login
            "password": "Pass123A",
        },
    )
    return res.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ----------------------------------------------------------
# Create Calculation
# ----------------------------------------------------------
def test_create_calculation():
    token = auth_token()

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={"type": "add", "a": 5, "b": 7},
    )

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["result"] == 12


# ----------------------------------------------------------
# List Calculations
# ----------------------------------------------------------
def test_list_calculations():
    token = auth_token()

    client.post(
        "/calculations",
        headers=auth_headers(token),
        json={"type": "multiply", "a": 3, "b": 4},
    )

    response = client.get("/calculations", headers=auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


# ----------------------------------------------------------
# Read Calculation
# ----------------------------------------------------------
def test_read_calculation():
    token = auth_token()

    create_res = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={"type": "subtract", "a": 20, "b": 3},
    )

    calc_id = create_res.json()["id"]

    response = client.get(f"/calculations/{calc_id}", headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["id"] == calc_id


# ----------------------------------------------------------
# Update Calculation
# ----------------------------------------------------------
def test_update_calculation():
    token = auth_token()

    create_res = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={"type": "add", "a": 1, "b": 1},
    )
    calc_id = create_res.json()["id"]

    response = client.put(
        f"/calculations/{calc_id}",
        headers=auth_headers(token),
        json={"type": "multiply", "a": 10, "b": 5},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["a"] == 10
    assert updated["b"] == 5
    assert updated["result"] == 50


# ----------------------------------------------------------
# Delete Calculation
# ----------------------------------------------------------
def test_delete_calculation():
    token = auth_token()

    create_res = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={"type": "divide", "a": 10, "b": 2},
    )
    calc_id = create_res.json()["id"]

    response = client.delete(f"/calculations/{calc_id}", headers=auth_headers(token))
    assert response.status_code == 204


# ----------------------------------------------------------
# Divide-by-zero error message must contain "zero"
# ----------------------------------------------------------
def test_invalid_divide_by_zero():
    token = auth_token()

    response = client.post(
        "/calculations",
        headers=auth_headers(token),
        json={"type": "divide", "a": 10, "b": 0},
    )

    assert response.status_code == 422

    detail = response.json()["detail"]
    # Handle validation error list or string
    if isinstance(detail, list):
        detail = detail[0].get("msg", "")

    assert "zero" in detail.lower()
