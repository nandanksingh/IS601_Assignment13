# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: User Schemas
# File: app/schemas/user_schema.py
# ----------------------------------------------------------
# Description:
#   • UserCreate  – full registration schema with compatibility
#     for Assignment-12 minimal registration (email + password only)
#   • UserLogin   – identifier/password for login
#   • UserResponse – full DB return model
#   • UserRead     – alias used by /auth/me
# ----------------------------------------------------------

from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
import re


# ----------------------------------------------------------
# Validators
# ----------------------------------------------------------
def validate_username(v: Optional[str]) -> Optional[str]:
    """Username is optional for backwards compatibility."""
    if v is None or v.strip() == "":
        return v  # Allowed because Assignment-12 sends no username
    if len(v) < 4:
        raise ValueError("Username must be at least 4 characters")
    if not re.match(r"^[A-Za-z0-9_]+$", v):
        raise ValueError("Username may only contain letters, numbers, underscores")
    return v


def validate_email(v: str) -> str:
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
        raise ValueError("Invalid email address")
    return v


def validate_mobile(v: Optional[str]) -> Optional[str]:
    if v and not re.match(r"^\d{10}$", v):
        raise ValueError("Mobile must be 10 digits")
    return v


def validate_password(v: str) -> str:
    if len(v) < 6:
        raise ValueError("Password must be at least 6 characters")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain a number")
    return v


# ----------------------------------------------------------
# Registration Schema
# ----------------------------------------------------------
class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None     # <- optional for old tests
    email: str
    mobile: Optional[str] = None
    password: str
    confirm_password: Optional[str] = None  # <- optional for old tests

    _username = field_validator("username")(validate_username)
    _email = field_validator("email")(validate_email)
    _mobile = field_validator("mobile")(validate_mobile)
    _password = field_validator("password")(validate_password)

    @field_validator("confirm_password")
    def confirm(cls, v, info):
        pwd = info.data.get("password")

        # If old test sends no confirm_password → do NOT block
        if v is None:
            return v

        if pwd is not None and v != pwd:
            raise ValueError("Passwords do not match")
        return v


# ----------------------------------------------------------
# Login Schema
# ----------------------------------------------------------
class UserLogin(BaseModel):
    identifier: str
    password: str

    @field_validator("identifier")
    def validate_identifier(cls, v):
        if not v or not v.strip():
            raise ValueError("Identifier cannot be empty")
        return v.strip()


# ----------------------------------------------------------
# DB Return Schema
# ----------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------
# Alias used for /auth/me
# ----------------------------------------------------------
class UserRead(UserResponse):
    pass
