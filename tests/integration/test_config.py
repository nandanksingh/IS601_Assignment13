# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-12: Configuration Module Integration Tests
# File: tests/integration/test_config.py
# ----------------------------------------------------------
# Description:
# Tests the configuration system responsible for environment
# flags, dynamic settings reload, and readable environment
# labels. Ensures environment variables are interpreted
# correctly and updated values are reflected across the app.
# ----------------------------------------------------------

import os
import pytest
from app.core.config import Settings, reload_settings, get_environment_mode


# ----------------------------------------------------------
# Environment flag evaluation
# ----------------------------------------------------------
def test_environment_flags(monkeypatch):
    """Verify the is_dev / is_prod / is_test flags for each ENV mode."""

    # Development mode flags
    monkeypatch.setenv("ENV", "development")
    s = Settings()
    assert s.is_dev is True
    assert s.is_prod is False
    assert s.is_test is False

    # Production mode flags
    monkeypatch.setenv("ENV", "production")
    s = Settings()
    assert s.is_prod is True
    assert s.is_dev is False
    assert s.is_test is False

    # Testing mode flags
    monkeypatch.setenv("ENV", "testing")
    s = Settings()
    assert s.is_test is True
    assert s.is_dev is False
    assert s.is_prod is False


# ----------------------------------------------------------
# reload_settings() behavior
# ----------------------------------------------------------
def test_reload_updates_values(monkeypatch):
    """Ensure reload_settings() rebuilds the global settings instance."""

    # Override environment variables before reload
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./changed.db")
    monkeypatch.setenv("SECRET_KEY", "newkey123")
    monkeypatch.setenv("ENV", "testing")

    updated = reload_settings()

    # Updated values must be reflected in new settings object
    assert updated.DATABASE_URL == "sqlite:///./changed.db"
    assert updated.SECRET_KEY == "newkey123"
    assert updated.is_test is True


# ----------------------------------------------------------
# get_environment_mode() mapping
# ----------------------------------------------------------
@pytest.mark.parametrize(
    "env_value, expected",
    [
        ("development", "development mode"),
        ("production", "production mode"),
        ("testing", "testing mode"),
        ("something_else", "Unknown environment"),
    ],
)
def test_print_environment_modes(env_value, expected):
    """Validate ENV → text label conversion."""
    assert expected.lower() in get_environment_mode(env_value).lower()
