# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Global Pytest Fixtures
# File: tests/conftest.py
# ----------------------------------------------------------
# Provides shared fixtures for all tests. Creates a clean
# isolated SQLite database, provides SQLAlchemy sessions,
# and generates realistic fake users including required
# fields such as email, mobile number, and password hash.
# Ensures all tests start with predictable and consistent
# database state across the full suite.
# ----------------------------------------------------------

import os
import pytest
from faker import Faker

# ----------------------------------------------------------
# Force test environment before importing application modules
# ----------------------------------------------------------
os.environ["ENV"] = "testing"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.database.dbase import Base, engine, SessionLocal
from app.models.user_model import User
from app.auth.security import hash_password

fake = Faker()
Faker.seed(12345)


# ----------------------------------------------------------
# Session-wide database initialization
# ----------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create tables once at the start of the test session."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ----------------------------------------------------------
# Reset database before each individual test
# ----------------------------------------------------------
@pytest.fixture(autouse=True)
def reset_db():
    """Ensure each test begins with a clean schema."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    pass


# ----------------------------------------------------------
# SQLAlchemy session fixture
# ----------------------------------------------------------
@pytest.fixture
def db_session():
    """Provide a new SQLAlchemy session for each test."""
    session = SessionLocal()
    try:
        yield session
        if session.is_active:
            try:
                session.commit()
            except Exception:
                session.rollback()
    finally:
        session.close()


# ----------------------------------------------------------
# Fake user data generator with required fields
# ----------------------------------------------------------
@pytest.fixture
def fake_user_data():
    """Return a valid fake User record for insertion."""
    return {
        "username": fake.unique.user_name(),
        "email": fake.unique.email(),
        "mobile": fake.unique.msisdn()[0:10],  # Ensure 10 digits
        "password_hash": hash_password("TestPass123"),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "is_active": True,
    }


# ----------------------------------------------------------
# Insert one test user into the database
# ----------------------------------------------------------
@pytest.fixture
def test_user(db_session, fake_user_data):
    """Insert a single user and return the instance."""
    user = User(**fake_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ----------------------------------------------------------
# Seed multiple users for list-based tests
# ----------------------------------------------------------
@pytest.fixture
def seed_users(db_session):
    """Insert several fake users and return the list."""
    users = []
    for _ in range(5):
        u = User(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            mobile=fake.msisdn()[0:10],
            password_hash=hash_password("TempPass123"),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_active=True,
        )
        db_session.add(u)
        users.append(u)

    db_session.commit()
    return users
