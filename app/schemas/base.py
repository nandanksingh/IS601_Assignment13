# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Schema Compatibility Layer
# File: app/schemas/base.py
# ----------------------------------------------------------
# Description:
# This module exists ONLY for backward-compatibility with older
# professor test suites (Assignment 10–12) that import:
#
#     from app.schemas.base import UserBase, UserCreate, UserLogin
#
# In Assignment 13, the actual schemas were reorganized into:
#     app/schemas/user_schema.py
#
# So this file RE-EXPORTS those classes and provides a minimal
# UserBase definition to satisfy legacy tests.
# ----------------------------------------------------------

from pydantic import BaseModel, Field, EmailStr, ConfigDict

# ----------------------------------------------------------
# Import the *actual* schemas used in the application
# ----------------------------------------------------------
from app.schemas.user_schema import UserCreate, UserLogin


# ----------------------------------------------------------
# Backward-compatible UserBase
# (old tests expect this exact minimal structure)
# ----------------------------------------------------------
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------
# Export list — ensures star imports work exactly like before
# ----------------------------------------------------------
__all__ = [
    "UserBase",
    "UserCreate",
    "UserLogin",
]
