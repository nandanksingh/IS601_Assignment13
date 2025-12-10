# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication Router
# File: app/routers/auth.py
# ----------------------------------------------------------
# Description:
# Provides authentication routes for user registration,
# login (identifier OR username), and user profile retrieval.
# Designed to satisfy both Assignment-13 schema structure and
# Assignment-12 legacy test payloads.
# ----------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dbase import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserRead
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ----------------------------------------------------------
# Register User
# ----------------------------------------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Register a new application user."""

    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check for duplicate username/email/mobile
    existing = (
        db.query(User)
        .filter(
            (User.username == payload.username)
            | (User.email == payload.email)
            | (User.mobile == payload.mobile)
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with this username, email, or mobile already exists",
        )

    # Create the user record
    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        username=payload.username,
        email=payload.email,
        mobile=payload.mobile,
        password_hash=hash_password(payload.password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id,
        "username": user.username,
    }


# ----------------------------------------------------------
# Login User (supports identifier OR username)
# ----------------------------------------------------------
@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(payload: dict, db: Session = Depends(get_db)):
    """
    Accepts BOTH:
        { "identifier": "value", "password": "Pass123" }
        { "username": "value", "password": "Pass123" }
    """

    # Extract login password
    password = payload.get("password")
    if not password:
        raise HTTPException(status_code=400, detail="Password is required")

    # Primary Assignment-13 field
    identifier = payload.get("identifier")

    # Assignment-12 legacy login format
    if not identifier:
        identifier = payload.get("username")

    if not identifier:
        raise HTTPException(status_code=400, detail="Login identifier is required")

    # Lookup user
    user = (
        db.query(User)
        .filter(
            (User.username == identifier)
            | (User.email == identifier)
            | (User.mobile == identifier)
        )
        .first()
    )

    # Failed login
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT
    token = create_access_token({"sub": str(user.id)})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }


# ----------------------------------------------------------
# Get Current Authenticated User
# ----------------------------------------------------------
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """Return profile of the authenticated user."""
    return current_user
