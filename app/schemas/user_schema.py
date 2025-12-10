# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: User Schemas
# File: app/schemas/user_schema.py
# ----------------------------------------------------------
# Description:
# Pydantic schemas supporting:
#   • First/last name
#   • Username, email, mobile validation
#   • Strong password rules + confirm password
#   • Login via identifier (username/email/mobile)
#   • ORM-friendly UserResponse and UserRead models
# ----------------------------------------------------------

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import re


# ----------------------------------------------------------
# Validation Helpers
# ----------------------------------------------------------
def validate_username(value: str) -> str:
    if len(value) < 4 or len(value) > 15:
        raise ValueError("Username must be 4–15 characters long")
    if not re.match(r"^[A-Za-z0-9_]+$", value):
        raise ValueError("Username may only contain letters, numbers, and underscores")
    return value


def validate_email(value: str) -> str:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, value):
        raise ValueError("Invalid email address")
    return value


def validate_mobile(value: str) -> str:
    if not re.match(r"^\d{10}$", value):
        raise ValueError("Mobile number must be exactly 10 digits")
    return value


def validate_password(value: str) -> str:
    if len(value) < 6 or len(value) > 20:
        raise ValueError("Password must be 6–20 characters long")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit")
    return value


# ----------------------------------------------------------
# User Registration Schema
# ----------------------------------------------------------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    mobile: str
    password: str
    confirm_password: str

    _username_validate = field_validator("username")(validate_username)
    _email_validate = field_validator("email")(validate_email)
    _mobile_validate = field_validator("mobile")(validate_mobile)
    _password_validate = field_validator("password")(validate_password)

    @field_validator("confirm_password")
    def validate_confirm_password(cls, v, info):
        password = info.data.get("password")
        if password is not None and v != password:
            raise ValueError("Passwords do not match")
        return v


# ----------------------------------------------------------
# Login Schema
# ----------------------------------------------------------
class UserLogin(BaseModel):
    identifier: Optional[str] = None
    password: str

    @field_validator("identifier")
    def validate_identifier(cls, v):
        if v is None or not str(v).strip():
            raise ValueError("Identifier cannot be empty")
        return v.strip()

    @field_validator("password")
    def validate_password_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Password cannot be empty")
        return v


# ----------------------------------------------------------
# Lightweight API Response Schema
# ----------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: Optional[str]
    mobile: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------
# UserRead Schema
# ----------------------------------------------------------
class UserRead(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: Optional[str]
    mobile: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
