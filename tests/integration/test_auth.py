# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication Tests (Full + Coverage Boost)
# File: tests/integration/test_auth.py
# ----------------------------------------------------------
# Description:
# Comprehensive test suite for authentication routes:
#   • Registration (/auth/register)
#   • Login (/auth/login)
#   • Current user (/auth/me)
# Includes additional coverage cases to reach 90–100%
# without modifying backend logic.
# ----------------------------------------------------------

from fastapi.testclient import TestClient
from main import app
from app.auth.security import decode_access_token_safe

client = TestClient(app)


# ==========================================================
# Helper Functions
# ==========================================================
def register_payload():
    """Default valid registration payload."""
    return {
        "first_name": "Test",
        "last_name": "User",
        "username": "test_user",
        "email": "test@example.com",
        "mobile": "1234567890",
        "password": "Pass123",
        "confirm_password": "Pass123",
    }


def register():
    """Helper to register the default test user."""
    return client.post("/auth/register", json=register_payload())


def login_with_email(password="Pass123"):
    """Login using email + password."""
    return client.post(
        "/auth/login",
        json={"identifier": "test@example.com", "password": password},
    )


def login_with_mobile(password="Pass123"):
    """Login using mobile number + password."""
    return client.post(
        "/auth/login",
        json={"identifier": "1234567890", "password": password},
    )


# ==========================================================
# Registration Tests
# ==========================================================
def test_register_success():
    response = register()
    assert response.status_code == 201

    data = response.json()
    assert data["message"] == "Registration successful"
    assert data["username"] == "test_user"


def test_register_duplicate_user():
    register()
    response = register()
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_register_auto_username():
    """Username auto-generated if empty (legacy behavior)."""
    payload = {
        "first_name": "Auto",
        "last_name": "User",
        "username": "",
        "email": "auto@example.com",
        "mobile": "1112223333",
        "password": "Pass123",
        "confirm_password": "Pass123",
    }

    res = client.post("/auth/register", json=payload)
    assert res.status_code == 201
    assert res.json()["username"].startswith("auto")


def test_register_without_confirm_password():
    """Support old tests where confirm_password was missing."""
    payload = {
        "first_name": "Old",
        "last_name": "Style",
        "username": "nostyle",
        "email": "nostyle@example.com",
        "mobile": "9998887777",
        "password": "Pass123",
        "confirm_password": None,
    }

    res = client.post("/auth/register", json=payload)
    assert res.status_code == 201
    assert res.json()["username"] == "nostyle"


# ==========================================================
# Login Tests
# ==========================================================
def test_login_success_with_email():
    register()
    response = login_with_email()
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_success_with_mobile():
    register()
    response = login_with_mobile()
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password():
    register()
    response = login_with_email(password="WrongPass")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_missing_identifier():
    """Ensure API rejects missing identifier."""
    res = client.post("/auth/login", json={"password": "Pass123"})
    assert res.status_code == 400
    assert "identifier" in res.json()["detail"]


def test_login_missing_password():
    """Ensure API rejects missing password."""
    res = client.post("/auth/login", json={"identifier": "test@example.com"})
    assert res.status_code == 400
    assert "Password" in res.json()["detail"]


def test_login_auto_create_test_user():
    """
    Auto-create the special Playwright test user if correct
    password provided (Assignment-12 compatibility).
    """
    res = client.post(
        "/auth/login",
        json={
            "identifier": "testuser_playwright@example.com",
            "password": "StrongPass123",
        },
    )

    data = res.json()
    assert res.status_code == 200
    assert "access_token" in data
    assert data["username"].startswith("testuser")


# ==========================================================
# /auth/me Test
# ==========================================================
def test_auth_me():
    register()
    token = login_with_email().json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test@example.com"


# ==========================================================
# JWT Decoder (Safe) Test
# ==========================================================
def test_invalid_token_does_not_raise_exception():
    """decode_access_token_safe must never throw errors."""
    result = decode_access_token_safe("invalid.token.data")
    assert isinstance(result, dict)
