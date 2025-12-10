# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Playwright E2E Tests
# File: tests/e2e/test_register.py
# ----------------------------------------------------------
# Description:
# End-to-end browser tests for the Registration page.
# Covers:
#   • Successful user registration
#   • Password validation (negative scenario)
# Uses Playwright + pytest to automate form input and UI checks.
# ----------------------------------------------------------

import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:8000"


@pytest.mark.e2e
def test_register_success(page: Page):
    """
    Positive Test:
    Register a new user with valid email and password.
    Expected:
        • Success message OR redirect behavior
        • No errors on the page
    """

    page.goto(f"{BASE_URL}/register")

    # Fill form fields
    page.fill("#email", "testuser_playwright@example.com")
    page.fill("#password", "StrongPass123")

    # Submit registration
    page.click("#registerBtn")

    # Wait for UI update
    page.wait_for_timeout(1000)

    # Check success response in UI
    message = page.inner_text("#registerMessage")
    assert (
        "success" in message.lower()
        or "created" in message.lower()
        or "registered" in message.lower()
    ), f"Unexpected register message: {message}"


@pytest.mark.e2e
def test_register_short_password(page: Page):
    """
    Negative Test:
    Register using a too-short password.
    Expected:
        • Error message appears on screen
    """

    page.goto(f"{BASE_URL}/register")

    page.fill("#email", "shortpass@example.com")
    page.fill("#password", "12")  # Too short

    page.click("#registerBtn")

    page.wait_for_timeout(800)

    message = page.inner_text("#registerMessage")
    assert (
        "password" in message.lower()
        or "short" in message.lower()
        or "invalid" in message.lower()
    ), f"Unexpected error message: {message}"
