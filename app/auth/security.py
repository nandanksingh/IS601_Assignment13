# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication & JWT Security Utilities
# File: app/auth/security.py
# ----------------------------------------------------------
# Description:
# Secure password hashing, verification, JWT creation,
# and safe decoding. Designed for Assignment 13, replacing
# Assignment-12 test-driven behaviors while maintaining
# backward-compatible helpers where useful.
# ----------------------------------------------------------

from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext

from app.core.config import settings


# ----------------------------------------------------------
# Password Hashing Context (bcrypt)
# ----------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------------------------------
# Password Hashing Utilities
# ----------------------------------------------------------
def hash_password(password: str) -> str:
    """Hash a raw password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(raw: str, hashed: str) -> bool:
    """Verify password safely without raising unexpected errors."""
    try:
        return pwd_context.verify(raw, hashed)
    except Exception:
        return False


def verify_password_hash(raw: str, hashed: str) -> bool:
    """
    Backward-compatible alias used by earlier test suites
    and assignment versions.
    """
    return verify_password(raw, hashed)


# ----------------------------------------------------------
# JWT Token Creation
# ----------------------------------------------------------
def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a signed JWT token containing user payload
    + expiration. If no custom expiration is provided,
    the value from settings is used.
    """
    payload = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["exp"] = expire

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


# ----------------------------------------------------------
# JWT Decoding (Safe)
# ----------------------------------------------------------
def decode_access_token(token: str) -> dict:
    """
    Safely decode a JWT token. NEVER raise exceptions.
    Return {} when token is invalid, expired, or malformed.
    This is the default decoder used across Assignment 13.
    """
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except Exception:
        return {}


# ----------------------------------------------------------
# Explicit Safe Decoder (Legacy Compatibility)
# ----------------------------------------------------------
def decode_access_token_safe(token: str) -> dict:
    """
    Legacy-safe JWT decoder that behaves identically to
    decode_access_token(), kept for backwards compatibility
    with older tests and utilities.
    """
    return decode_access_token(token)
