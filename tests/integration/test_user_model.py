# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: User Model Tests
# File: tests/integration/test_user_model.py
# ----------------------------------------------------------
# Description:
# Integration tests for the SQLAlchemy User model including
# inserts, updates, rollbacks, unique constraints, password
# hashing and verification, schema conversion, and safe repr
# behavior. Ensures ORM correctness in a controlled test DB.
# ----------------------------------------------------------

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.user_model import User
from app.database.dbase import Base, engine, SessionLocal
from app.auth.security import hash_password


# ----------------------------------------------------------
# Database setup / teardown
# ----------------------------------------------------------
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Drop and recreate all tables for isolated test runs."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide a fresh SQLAlchemy session per test."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ----------------------------------------------------------
# User factory fixture
# ----------------------------------------------------------
@pytest.fixture
def make_user():
    """Factory to generate valid user objects."""
    def _make(username, email, mobile="9998887777"):
        return User(
            username=username,
            email=email,
            mobile=mobile,           # mobile is now required in model
            first_name="Test",
            last_name="User",
            password_hash=hash_password("Secure123A"),
        )
    return _make


# ----------------------------------------------------------
# Core model tests
# ----------------------------------------------------------
def test_database_connection(db_session):
    assert db_session.execute(text("SELECT 1")).scalar() == 1


def test_user_commit_and_rollback(db_session, make_user):
    u1 = make_user("alpha", "alpha@example.com")
    db_session.add(u1)
    db_session.commit()

    # Attempt duplicate email → unique constraint
    u2 = make_user("beta", "alpha@example.com")
    db_session.add(u2)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    assert db_session.query(User).count() == 1


def test_user_query_methods(db_session, make_user):
    db_session.add_all([
        make_user("user1", "u1@example.com"),
        make_user("user2", "u2@example.com"),
        make_user("user3", "u3@example.com"),
    ])
    db_session.commit()

    result = db_session.query(User).filter_by(username="user2").first()
    assert result.email == "u2@example.com"


def test_user_update_and_refresh(db_session, make_user):
    user = make_user("nandan", "nandan@example.com")
    db_session.add(user)
    db_session.commit()

    user.email = "updated@example.com"
    db_session.commit()
    db_session.refresh(user)

    assert user.email == "updated@example.com"


@pytest.mark.slow
def test_bulk_user_insert(db_session, make_user):
    users = [make_user(f"bulk{i}", f"bulk{i}@example.com") for i in range(5)]
    db_session.bulk_save_objects(users)
    db_session.commit()

    assert db_session.query(User).count() >= 5


def test_unique_constraints(db_session, make_user):
    db_session.add(make_user("dup", "dup@example.com"))
    db_session.commit()

    with pytest.raises(IntegrityError):
        db_session.add(make_user("dup", "new@example.com"))
        db_session.commit()


def test_transaction_rollback(db_session, make_user):
    user = make_user("roll", "roll@example.com")
    db_session.add(user)
    db_session.commit()

    # Induce SQL error
    with pytest.raises(SQLAlchemyError):
        db_session.execute(text("SELECT * FROM non_existing_table"))
        db_session.commit()

    db_session.rollback()

    assert db_session.query(User).filter_by(username="roll").first() is not None


# ----------------------------------------------------------
# Password tests
# ----------------------------------------------------------
def test_user_password_methods(db_session):
    user = User(
        username="demo",
        email="demo@example.com",
        mobile="7776665555",
        first_name="A",
        last_name="B",
    )
    user.set_password("Secure123A")

    db_session.add(user)
    db_session.commit()

    assert user.verify_password("Secure123A")
    assert not user.verify_password("wrong")


# ----------------------------------------------------------
# Schema conversion tests
# ----------------------------------------------------------
def test_user_to_read_schema(db_session, make_user):
    user = make_user("convert", "convert@example.com")
    db_session.add(user)
    db_session.commit()

    schema = user.to_read_schema()
    assert schema.username == "convert"
    assert schema.email == "convert@example.com"
    assert schema.mobile == "9998887777"


# ----------------------------------------------------------
# repr() must never crash
# ----------------------------------------------------------
def test_user_repr_never_crashes(db_session, make_user):
    user = make_user("repr", "repr@example.com")
    db_session.add(user)
    db_session.commit()

    # Delete non-critical field to simulate corruption
    del user.email

    output = repr(user)
    assert "User" in output
    assert isinstance(output, str)
