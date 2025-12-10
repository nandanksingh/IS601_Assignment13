# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Playwright E2E Tests
# File: tests/e2e/test_login.py
# ----------------------------------------------------------
# Description:
# End-to-end browser tests for the Login page.
# Covers:
#   • Successful login (valid credentials)
#   • Incorrect login attempt (invalid password)
# Verifies UI messages and JWT token storage.
# ----------------------------------------------------------

import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:8000"


@pytest.mark.e2e
def test_login_success(page: Page):
    """
    Positive Test:
    Login using valid existing credentials.
    Expected:
        • Success message
        • JWT token saved in localStorage
    """

    page.goto(f"{BASE_URL}/login")

    page.fill("#email", "testuser_playwright@example.com")
    page.fill("#password", "StrongPass123")

    page.click("#loginBtn")
    page.wait_for_timeout(1000)

    # UI confirmation
    message = page.inner_text("#loginMessage")
    assert (
        "success" in message.lower()
        or "welcome" in message.lower()
        or "logged" in message.lower()
    ), f"Unexpected login message: {message}"

    # Check token stored in localStorage
    token = page.evaluate("localStorage.getItem('access_token')")
    assert token is not None, "Token was not stored!"
    assert len(token) > 20, "Token length too short — invalid token."


@pytest.mark.e2e
def test_login_wrong_password(page: Page):
    """
    Negative Test:
    Attempt login using wrong password.
    Expected:
        • Error message rendered on UI
        • No token saved in localStorage
    """

    page.goto(f"{BASE_URL}/login")

    page.fill("#email", "testuser_playwright@example.com")
    page.fill("#password", "WrongPass999")

    page.click("#loginBtn")
    page.wait_for_timeout(800)

    message = page.inner_text("#loginMessage")
    assert (
        "invalid" in message.lower()
        or "wrong" in message.lower()
        or "unauthorized" in message.lower()
    ), f"Unexpected error message: {message}"

    # Ensure token NOT stored
    token = page.evaluate("localStorage.getItem('access_token')")
    assert token is None
