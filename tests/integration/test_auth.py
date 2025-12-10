# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication Tests
# File: tests/integration/test_auth.py
# ----------------------------------------------------------
# Description:
# Updated for Assignment 13 API design:
#   • Registration requires: username, email, mobile,
#     first_name, last_name, password, confirm_password
#   • Login uses identifier (email OR mobile) + password
#   • Register returns 201
#   • Login returns access_token
#   • /auth/me returns authenticated user profile
# ----------------------------------------------------------

from fastapi.testclient import TestClient
from main import app
from app.auth.security import decode_access_token_safe

client = TestClient(app)


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------
def register_payload():
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
    return client.post("/auth/register", json=register_payload())


def login_with_email(password="Pass123"):
    return client.post(
        "/auth/login",
        json={"identifier": "test@example.com", "password": password},
    )


def login_with_mobile(password="Pass123"):
    return client.post(
        "/auth/login",
        json={"identifier": "1234567890", "password": password},
    )


# ----------------------------------------------------------
# Registration Tests
# ----------------------------------------------------------
def test_register_success():
    response = register()
    assert response.status_code == 201

    data = response.json()
    assert data["message"] == "Registration successful"
    assert data["username"] == "test_user"
    assert "user_id" in data


def test_register_duplicate_user():
    register()
    response = register()
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


# ----------------------------------------------------------
# Login Tests
# ----------------------------------------------------------
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


# ----------------------------------------------------------
# /auth/me test
# ----------------------------------------------------------
def test_auth_me():
    register()
    token = login_with_email().json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "test_user"
    assert body["email"] == "test@example.com"


# ----------------------------------------------------------
# Safe JWT Decoder Test
# ----------------------------------------------------------
def test_invalid_token_does_not_raise_exception():
    result = decode_access_token_safe("invalid.token.data")
    assert isinstance(result, dict)
