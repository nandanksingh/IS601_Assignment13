# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Calculator Route Tests
# File: tests/integration/test_rout_calc.py
# ----------------------------------------------------------
# Description:
# Tests calculation creation and retrieval through the
# router layer. Ensures correct HTTP behavior, JSON shape,
# and result computation.
# ----------------------------------------------------------

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_and_read_calculation():
    # Register user
    client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "username": "calc_test",
            "email": "calc_test@example.com",
            "password": "Pass123",
            "confirm_password": "Pass123",
            "mobile": "1234567890"
        },
    )

    # Login using Assignment-13 style ("identifier")
    token = client.post(
        "/auth/login",
        json={"identifier": "calc_test", "password": "Pass123"},
    ).json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create a calculation
    create_res = client.post(
        "/calculations",
        json={"type": "add", "a": 5, "b": 3},
        headers=headers,
    )

    assert create_res.status_code == 201
    data = create_res.json()

    assert "id" in data
    assert data["result"] == 8
    calc_id = data["id"]

    # Read back the calculation
    read_res = client.get(f"/calculations/{calc_id}", headers=headers)

    assert read_res.status_code == 200
    read_data = read_res.json()

    assert read_data["id"] == calc_id
    assert read_data["result"] == 8
    assert read_data["a"] == 5
    assert read_data["b"] == 3
    assert read_data["type"].lower() == "add"
