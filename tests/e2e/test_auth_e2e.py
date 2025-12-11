# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication E2E Tests
# File: tests/e2e/test_auth_e2e.py
# ----------------------------------------------------------
# Description:
# End-to-end Playwright tests validating homepage rendering,
# user registration, login, token storage, and navigation.
# Tests ensure UI and API work together seamlessly.
# ----------------------------------------------------------

import os
import time
import pytest
import requests
from playwright.sync_api import sync_playwright

# E2E Base URL (local run)
BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000")


# ----------------------------------------------------------
# Wait for FastAPI Server Ready
# ----------------------------------------------------------
def wait_for_app_ready(url=f"{BASE_URL}/health", timeout=30):
    """Polls the /health endpoint until FastAPI is running."""
    for _ in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("FastAPI is ready.")
                return
        except Exception:
            pass
        time.sleep(1)

    pytest.fail("FastAPI failed to start")


# ----------------------------------------------------------
# Playwright Fixtures
# ----------------------------------------------------------
@pytest.fixture(scope="module")
def browser():
    wait_for_app_ready()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


# ----------------------------------------------------------
# HOMEPAGE TEST
# ----------------------------------------------------------
@pytest.mark.e2e
def test_homepage_loads(page):
    page.goto(BASE_URL)
    body = page.text_content("body") or ""
    assert "Welcome to Nandan's Calculations App" in body


# ----------------------------------------------------------
# REGISTRATION TESTS
# ----------------------------------------------------------
@pytest.mark.e2e
def test_register_positive(page):
    """Successful registration should show success message."""
    page.goto(f"{BASE_URL}/register")

    page.fill("#username", "testuser123")
    page.fill("#email", "test@example.com")
    page.fill("#mobile", "1234567890")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "TestPass123")
    page.fill("#confirm_password", "TestPass123")

    page.click("#registerBtn")

    # Updated selector: correct ID is #message
    page.wait_for_selector("#message", timeout=5000)
    msg = page.text_content("#message") or ""
    assert "Registration successful" in msg


@pytest.mark.e2e
def test_register_password_mismatch(page):
    """Client-side mismatch check should show an error message."""
    page.goto(f"{BASE_URL}/register")

    page.fill("#username", "baduser1")
    page.fill("#email", "bad@example.com")
    page.fill("#mobile", "1234567890")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "Password1")
    page.fill("#confirm_password", "WrongPassword")

    page.click("#registerBtn")

    page.wait_for_selector("#message", timeout=5000)
    msg = page.text_content("#message") or ""
    assert "match" in msg.lower()


# ----------------------------------------------------------
# LOGIN TESTS
# ----------------------------------------------------------
@pytest.mark.e2e
def test_login_positive(page):
    """Valid login should store JWT token and load dashboard."""
    page.goto(f"{BASE_URL}/login")

    page.fill("#email_or_mobile", "test@example.com")
    page.fill("#password", "TestPass123")

    page.click("#loginBtn")

    page.wait_for_selector("#login_message", timeout=5000)
    msg = page.text_content("#login_message") or ""
    assert "Login successful" in msg

    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is not None
    assert len(token) > 20

    page.wait_for_timeout(1500)
    body = page.text_content("body") or ""
    assert "Calculations Dashboard" in body


@pytest.mark.e2e
def test_login_invalid_password(page):
    page.goto(f"{BASE_URL}/login")

    page.fill("#email_or_mobile", "test@example.com")
    page.fill("#password", "WrongPassword")

    page.click("#loginBtn")

    page.wait_for_selector("#login_message", timeout=5000)
    msg = page.text_content("#login_message") or ""
    assert "invalid" in msg.lower()


@pytest.mark.e2e
def test_login_unknown_user(page):
    page.goto(f"{BASE_URL}/login")

    page.fill("#email_or_mobile", "nouser@example.com")
    page.fill("#password", "SomePass123")

    page.click("#loginBtn")

    page.wait_for_selector("#login_message", timeout=5000)
    msg = page.text_content("#login_message") or ""
    assert "invalid" in msg.lower()
