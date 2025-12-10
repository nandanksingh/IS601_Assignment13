# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Central Application Configuration
# File: app/core/config.py
# ----------------------------------------------------------
# Description:
# Centralized configuration used across the FastAPI project.
# Provides:
#   • Database connection settings
#   • JWT security configuration
#   • Application runtime mode
#   • Reload helpers for tests
# ----------------------------------------------------------

import os
from pydantic_settings import BaseSettings


# ----------------------------------------------------------
# Settings Container (Pydantic v2)
# ----------------------------------------------------------
class Settings(BaseSettings):
    """Main settings object loaded from environment variables or `.env`."""

    # ------------------------------------------------------
    # Database Configuration
    # ------------------------------------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # ------------------------------------------------------
    # JWT Security Configuration
    # ------------------------------------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key-assignment13")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # ------------------------------------------------------
    # Application Environment
    # ------------------------------------------------------
    ENV: str = os.getenv("ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # ------------------------------------------------------
    # Convenience Flags
    # ------------------------------------------------------
    @property
    def is_dev(self) -> bool:
        return self.ENV.lower() == "development"

    @property
    def is_prod(self) -> bool:
        return self.ENV.lower() == "production"

    @property
    def is_test(self) -> bool:
        return self.ENV.lower() == "testing"

    # ------------------------------------------------------
    # Pydantic Model Config
    # ------------------------------------------------------
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


# Global settings instance used throughout the application
settings = Settings()


# ----------------------------------------------------------
# Test Utility Hooks
# ----------------------------------------------------------
def reload_settings() -> Settings:
    """
    Reload settings after environment variable changes.
    This is used by test suites that adjust ENV or token
    configuration at runtime.
    """
    global settings
    settings = Settings()
    return settings


def get_environment_mode(env: str) -> str:
    """Convert raw ENV string into a human-readable label."""
    env = (env or "").lower()

    if env == "development":
        return "development mode"
    elif env == "production":
        return "production mode"
    elif env == "testing":
        return "testing mode"

    return "Unknown environment"
