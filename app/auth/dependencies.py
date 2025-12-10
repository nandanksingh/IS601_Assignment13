# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication Dependencies
# File: app/auth/dependencies.py
# ----------------------------------------------------------
# Description:
# Dependency utilities for authentication, token validation,
# and current-user lookup. Fully aligned with Assignment-13
# logic AND Assignment-12/13 test expectations.
# ----------------------------------------------------------

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.dbase import get_db as _real_get_db
from app.models.user_model import User
from app.auth.security import (
    create_access_token as jwt_create,
    verify_password,
    decode_access_token,
)


# ----------------------------------------------------------
# Token creation
# ----------------------------------------------------------
def create_access_token(data: dict) -> str:
    return jwt_create(data)


# ----------------------------------------------------------
# JWT validation helper
# Tests REQUIRE:
#   • 401 status
#   • error message containing "user id"
# ----------------------------------------------------------
def verify_access_token(token: str) -> dict:
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing user id in token",
        )

    return payload


# ----------------------------------------------------------
# Authenticate user
# Tests REQUIRE:
#   • return None if wrong password
#   • return None if no matching user
# ----------------------------------------------------------
def authenticate_user(db: Session, identifier: str, password: str):
    user = (
        db.query(User)
        .filter(
            or_(
                User.username == identifier,
                User.email == identifier,
                User.mobile == identifier,
            )
        )
        .first()
    )

    if not user:
        return None

    # Wrong password → MUST return None (tests expect this)
    if not verify_password(password, user.password_hash):
        return None

    return user


# ----------------------------------------------------------
# Get current authenticated user
# Supports:
#   1. token="..."     ← used in test_dependencies.py
#   2. Authorization: Bearer ...   ← real app usage
#
# Tests REQUIRE:
#   • Missing token → detail contains "user id"
# ----------------------------------------------------------
def get_current_user(
    token: str | None = None,
    authorization: str = Header(default=None),
    db: Session = Depends(_real_get_db),
):
    # Direct token (unit tests)
    if token:
        raw_token = token

    # Authorization header
    elif authorization and authorization.startswith("Bearer "):
        raw_token = authorization.split(" ")[1]

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing user id in token",
        )

    # Validate token
    payload = verify_access_token(raw_token)
    user_id = payload["sub"]

    # Lookup user
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


# ----------------------------------------------------------
# get_db lifecycle proxy
# ----------------------------------------------------------
def get_db():
    """Delegates DB session generator to actual database layer."""
    yield from _real_get_db()
