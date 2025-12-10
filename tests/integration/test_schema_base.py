# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Updated Schema Tests
# File: tests/integration/test_schema_base.py
# ----------------------------------------------------------
# Description:
# Updated to match the Assignment-13 schema architecture.
# Tests validation rules inside:
#   • UserCreate
#   • UserLogin
#   • Username / email / mobile validation
#   • Password strength validation
# ----------------------------------------------------------

import pytest
from pydantic import ValidationError

from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
)


# ----------------------------------------------------------
# UserCreate Tests
# ----------------------------------------------------------
def test_user_create_valid():
    """Valid user registration input should succeed."""
    data = {
        "first_name": "Nandan",
        "last_name": "Kumar",
        "username": "nandan123",
        "email": "nandan@example.com",
        "mobile": "1234567890",
        "password": "StrongPass1",
        "confirm_password": "StrongPass1",
    }

    user = UserCreate(**data)

    assert user.username == "nandan123"
    assert user.email == "nandan@example.com"
    assert user.mobile == "1234567890"


def test_user_create_password_mismatch():
    """Passwords must match."""
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "email": "test@example.com",
        "mobile": "1234567890",
        "password": "StrongPass1",
        "confirm_password": "WrongPass1",
    }

    with pytest.raises(ValidationError):
        UserCreate(**data)


@pytest.mark.parametrize("username", ["ab", "a", "invalid space", "bad!char"])
def test_user_create_invalid_username(username):
    """Username must follow validation rules."""
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": username,
        "email": "test@example.com",
        "mobile": "1234567890",
        "password": "StrongPass1",
        "confirm_password": "StrongPass1",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_create_invalid_email():
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "gooduser",
        "email": "invalid-email",
        "mobile": "1234567890",
        "password": "StrongPass1",
        "confirm_password": "StrongPass1",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_create_invalid_mobile():
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "gooduser",
        "email": "test@example.com",
        "mobile": "12345",     # wrong length
        "password": "StrongPass1",
        "confirm_password": "StrongPass1",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


@pytest.mark.parametrize(
    "password",
    ["short", "nocaps123", "NOLOWER123", "NoDigitsHere"]
)
def test_user_create_invalid_password(password):
    """Password must meet all strength rules."""
    data = {
        "first_name": "Test",
        "last_name": "User",
        "username": "gooduser",
        "email": "test@example.com",
        "mobile": "1234567890",
        "password": password,
        "confirm_password": password,
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)


# ----------------------------------------------------------
# UserLogin Tests
# ----------------------------------------------------------
def test_user_login_valid():
    """Valid login should pass (identifier = email or mobile)."""
    schema = UserLogin(identifier="nandan@example.com", password="StrongPass1")
    assert schema.identifier == "nandan@example.com"
    assert schema.password == "StrongPass1"


def test_user_login_missing_fields():
    with pytest.raises(ValidationError):
        UserLogin(identifier=None, password="StrongPass1")  # type: ignore

    with pytest.raises(ValidationError):
        UserLogin(identifier="nandan@example.com", password=None)  # type: ignore


def test_user_login_reject_empty_strings():
    with pytest.raises(ValidationError):
        UserLogin(identifier="", password="StrongPass1")

    with pytest.raises(ValidationError):
        UserLogin(identifier="nandan@example.com", password="")


