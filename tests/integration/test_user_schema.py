# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: User Schema Tests
# File: tests/integration/test_user_schema.py
# ----------------------------------------------------------
# Description:
# Tests validation behavior of Assignment-13 user schemas,
# including field requirements, email and mobile formatting,
# password rules, confirm password match, login identifier
# rules, and safe response/read serialization.
# ----------------------------------------------------------

import pytest
from pydantic import ValidationError

from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserRead,
    UserResponse,
)


# ----------------------------------------------------------
# UserCreate – Valid Case
# ----------------------------------------------------------
def test_user_create_valid():
    """UserCreate should accept fully valid registration input."""
    schema = UserCreate(
        username="nk123",
        email="nandan@example.com",
        mobile="9998887777",
        password="Strong123A",
        confirm_password="Strong123A",
        first_name="Nandan",
        last_name="Kumar",
    )
    assert schema.username == "nk123"
    assert schema.mobile == "9998887777"


# ----------------------------------------------------------
# Invalid Password Cases
# ----------------------------------------------------------
@pytest.mark.parametrize(
    "password",
    ["short", "nocaps123", "NOLOWER123", "NoNumber"],
)
def test_user_create_invalid_password(password):
    """UserCreate must reject weak or non-compliant passwords."""
    with pytest.raises(ValidationError):
        UserCreate(
            username="user1",
            email="good@example.com",
            mobile="9998887777",
            password=password,
            confirm_password=password,
            first_name="A",
            last_name="B",
        )


# ----------------------------------------------------------
# Confirm Password Mismatch
# ----------------------------------------------------------
def test_user_create_confirm_password_mismatch():
    with pytest.raises(ValidationError):
        UserCreate(
            username="user1",
            email="valid@example.com",
            mobile="9998887777",
            password="Strong123A",
            confirm_password="Wrong123A",
            first_name="Test",
            last_name="User",
        )


# ----------------------------------------------------------
# Invalid Email
# ----------------------------------------------------------
def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="userx",
            email="invalid-email",
            mobile="9998887777",
            password="Strong123A",
            confirm_password="Strong123A",
            first_name="A",
            last_name="B",
        )


# ----------------------------------------------------------
# Invalid Mobile Number
# ----------------------------------------------------------
@pytest.mark.parametrize("mobile", ["12345", "abcdefghij", "12345678901"])
def test_user_create_invalid_mobile(mobile):
    with pytest.raises(ValidationError):
        UserCreate(
            username="userx",
            email="valid@example.com",
            mobile=mobile,
            password="Strong123A",
            confirm_password="Strong123A",
            first_name="A",
            last_name="B",
        )


# ----------------------------------------------------------
# UserLogin Schema
# ----------------------------------------------------------
def test_user_login_valid():
    """UserLogin accepts identifier (email or mobile) + password."""
    schema = UserLogin(identifier="user@example.com", password="Strong123A")
    assert schema.identifier == "user@example.com"


def test_user_login_invalid_missing_identifier():
    with pytest.raises(ValidationError):
        UserLogin(identifier="", password="Strong123A")


# ----------------------------------------------------------
# UserRead Schema
# ----------------------------------------------------------
def test_user_read_schema():
    """UserRead should serialize minimal safe fields."""
    schema = UserRead(
        id=1,
        username="nk123",
        email="nk@example.com",
        mobile="9998887777",
        first_name="Nandan",
        last_name="Kumar",
        is_active=True,
    )
    assert schema.id == 1
    assert schema.username == "nk123"


# ----------------------------------------------------------
# UserResponse Schema
# ----------------------------------------------------------
def test_user_response_schema():
    """UserResponse returns public profile fields."""
    schema = UserResponse(
        id=10,
        username="alpha",
        email="test@example.com",
        mobile="9876543210",
        first_name="Alpha",
        last_name="User",
        is_active=True,
    )
    assert schema.username == "alpha"
    assert schema.mobile == "9876543210"
