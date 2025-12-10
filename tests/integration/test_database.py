# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: Database Integration Tests
# File: tests/integration/test_database.py
# ----------------------------------------------------------
# Description:
# Comprehensive test suite validating the database layer.
# Ensures engine creation paths, URL handling, session
# lifecycle behavior, init/drop operations, and fallback
# helpers all execute correctly. Covers both success and
# failure branches for reliable database infrastructure.
# ----------------------------------------------------------

import os
import sys
import pytest
import importlib
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

DATABASE_MODULE = "app.database.dbase"


# ----------------------------------------------------------
# Reload helper for fresh environment per test
# ----------------------------------------------------------
def reload_database_module():
    if DATABASE_MODULE in sys.modules:
        del sys.modules[DATABASE_MODULE]
    return importlib.import_module(DATABASE_MODULE)


# ----------------------------------------------------------
# Engine + URL Tests
# ----------------------------------------------------------
def test_get_engine_success(monkeypatch):
    """A valid SQLite engine must be created."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    db = reload_database_module()
    engine = db.get_engine()
    assert isinstance(engine, Engine)


def test_get_engine_failure_with_sqlite(monkeypatch):
    """Force create_engine() to raise an error → must bubble up."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")

    with patch(
        "app.database.dbase.create_engine",
        side_effect=SQLAlchemyError("Simulated failure")
    ):
        import app.database.dbase as dbase
        with pytest.raises(SQLAlchemyError):
            dbase.get_engine()


def test_get_engine_coverage_fallback(monkeypatch):
    """Ensure engine URL is properly resolved under SQLite."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    db = reload_database_module()
    engine = db.get_engine()
    assert "sqlite" in str(engine.url)


def test_get_database_url_variants(monkeypatch):
    """Verify DATABASE_URL supports PostgreSQL or SQLite."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@db:5432/test_db")
    import app.database.dbase as dbase
    result = dbase.get_database_url()
    assert "postgresql" in result or "sqlite" in result


# ----------------------------------------------------------
# Session Lifecycle
# ----------------------------------------------------------
def test_session_factory():
    """SessionLocal must return a valid SQLAlchemy session."""
    db = reload_database_module()
    session = db.SessionLocal()
    assert isinstance(session, Session)
    session.close()


def test_base_declaration():
    """Verify Base metadata exists."""
    db = reload_database_module()
    assert db.Base is not None


def test_init_drop_db():
    """init_db() and drop_db() must call metadata operations."""
    db = reload_database_module()
    with patch.object(db.Base.metadata, "create_all") as mock_create, \
            patch.object(db.Base.metadata, "drop_all") as mock_drop:
        db.init_db()
        db.drop_db()
        assert mock_create.called
        assert mock_drop.called


def test_run_session_lifecycle_success(monkeypatch):
    """Successful commit path for lifecycle coverage."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "dummy")
    import app.database.dbase as dbase
    dbase._run_session_lifecycle_for_coverage()


def test_run_session_lifecycle_failure(monkeypatch):
    """Simulate failure in get_session() → expect RuntimeError."""
    import app.database.dbase as dbase
    with patch("app.database.dbase.get_session", side_effect=Exception("session fail")):
        with pytest.raises(RuntimeError):
            dbase._run_session_lifecycle_for_coverage()


# ----------------------------------------------------------
# PostgreSQL Fallback Helpers
# ----------------------------------------------------------
import app.database.dbase as db_init


def test_postgres_unavailable_true():
    """Socket connection failure → postgres considered unavailable."""
    with patch("socket.create_connection", side_effect=OSError()):
        assert db_init._postgres_unavailable() is True


def test_postgres_unavailable_false():
    """Successful socket connection → postgres reachable."""
    mock_conn = MagicMock()
    with patch("socket.create_connection", return_value=mock_conn):
        assert db_init._postgres_unavailable() is False


def test_ensure_sqlite_fallback(monkeypatch):
    """Fallback replaces DATABASE_URL with SQLite when PG unreachable."""
    monkeypatch.setenv("DATABASE_URL", "postgres://x")
    with patch("app.database.dbase._postgres_unavailable", return_value=True):
        db_init._ensure_sqlite_fallback()
        assert "sqlite" in os.getenv("DATABASE_URL")


def test_trigger_fallback_executes(monkeypatch):
    """Trigger fallback effect in test environment."""
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "dummy")
    monkeypatch.setenv("DATABASE_URL", "postgres://x")

    with patch("app.database.dbase._postgres_unavailable", return_value=True):
        db_init._trigger_fallback_if_test_env()
        assert "sqlite" in os.getenv("DATABASE_URL")


def test_trigger_fallback_error(monkeypatch):
    """If fallback operation fails → RuntimeError expected."""
    import app.database.dbase as db

    def boom():
        raise Exception("fail")

    monkeypatch.setattr(db, "_ensure_sqlite_fallback", boom)

    with pytest.raises(RuntimeError):
        db._trigger_fallback_if_test_env()
