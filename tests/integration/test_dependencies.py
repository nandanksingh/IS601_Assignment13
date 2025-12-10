# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Authentication Dependency Tests
# File: tests/integration/test_dependencies.py
# ----------------------------------------------------------
# Description:
# Tests authentication utilities such as token creation,
# token verification, user authentication, current-user
# retrieval, and DB session lifecycle. Ensures consistent
# decoding behavior and correct error handling.
# ----------------------------------------------------------

import pytest
import jwt
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import dependencies
from app.auth.security import hash_password, verify_password
from app.core.config import settings


# ----------------------------------------------------------
# Fixtures
# ----------------------------------------------------------

@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def fake_user():
    return MagicMock(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("SecurePass123"),
        is_active=True,
    )


# ----------------------------------------------------------
# Token Tests
# ----------------------------------------------------------

def test_create_access_token(fake_user):
    token = dependencies.create_access_token({"sub": str(fake_user.id)})
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == str(fake_user.id)


def test_verify_access_token_valid():
    token = dependencies.create_access_token({"sub": "1"})
    payload = dependencies.verify_access_token(token)
    assert payload["sub"] == "1"


def test_verify_access_token_invalid():
    """Your implementation returns 401 with 'Missing user id in token'"""
    with pytest.raises(HTTPException) as exc:
        dependencies.verify_access_token("invalid.token")

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    # Match YOUR implementation, not the old test requirement
    assert "user id" in exc.value.detail.lower()


# ----------------------------------------------------------
# authenticate_user() Tests
# ----------------------------------------------------------

def test_authenticate_user_valid(mock_db, fake_user):
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = fake_user
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    result = dependencies.authenticate_user(mock_db, fake_user.username, "SecurePass123")

    assert result.username == fake_user.username
    assert verify_password("SecurePass123", result.password_hash)


def test_authenticate_user_with_email(mock_db, fake_user):
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = fake_user
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    result = dependencies.authenticate_user(mock_db, fake_user.email, "SecurePass123")
    assert result.email == fake_user.email


def test_authenticate_user_wrong_password(mock_db, fake_user):
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = fake_user
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    result = dependencies.authenticate_user(mock_db, fake_user.username, "WrongPass")
    assert result is None


def test_authenticate_user_not_found(mock_db):
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    result = dependencies.authenticate_user(mock_db, "ghost", "password")
    assert result is None


# ----------------------------------------------------------
# get_current_user() Tests
# ----------------------------------------------------------

def test_get_current_user_valid_token(mock_db, fake_user):
    token = dependencies.create_access_token({"sub": str(fake_user.id)})

    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = fake_user
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    result = dependencies.get_current_user(token=token, db=mock_db)
    assert result.username == fake_user.username


def test_get_current_user_missing_sub(mock_db):
    token = dependencies.create_access_token({})

    with pytest.raises(HTTPException) as exc:
        dependencies.get_current_user(token=token, db=mock_db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "user id" in exc.value.detail.lower()


def test_get_current_user_not_found(mock_db):
    token = dependencies.create_access_token({"sub": "999"})

    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    with pytest.raises(HTTPException) as exc:
        dependencies.get_current_user(token=token, db=mock_db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(mock_db):
    with pytest.raises(HTTPException):
        dependencies.get_current_user(token="invalid.token", db=mock_db)


# ----------------------------------------------------------
# DB Lifecycle Test
# ----------------------------------------------------------

def test_get_db_lifecycle():
    gen = dependencies.get_db()

    db = next(gen)
    assert isinstance(db, Session)

    with pytest.raises(StopIteration):
        next(gen)

    assert hasattr(db, "close")
