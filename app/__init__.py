# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment-13: Application Package Initializer
# File: app/__init__.py
# ----------------------------------------------------------
# Description:
# Marks the "app" directory as a Python package and provides
# a BASE_DIR constant used for path resolution across the
# project. Ensures consistent imports for Docker, pytest,
# CI/CD, and general application modules.
# ----------------------------------------------------------

from pathlib import Path

# Root directory of the application package
BASE_DIR = Path(__file__).resolve().parent

__all__ = ["BASE_DIR"]
