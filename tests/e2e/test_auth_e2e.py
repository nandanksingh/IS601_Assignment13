# ----------------------------------------------------------
# Author: Nandan Kumar
# Assignment 13: Authentication E2E Tests
# File: tests/e2e/test_auth_e2e.py
# ----------------------------------------------------------
# Description:
# End-to-end Playwright tests validating homepage, user
# registration, login using email or mobile, token storage,
# and successful navigation to the dashboard.
# Ensures front-end and back-end routes work together.
# ----------------------------------------------------------

import os
import time
import pytest
import requests
from playwright.sync_api import sync_playwright


BASE_URL = os.getenv("E2E_BASE_URL", "http://app:8000")


# ----------------------------------------------------------
# Wait for FastAPI to start
# ----------------------------------------------------------
def wait_for_app_ready(url=f"{BASE_URL}/health", timeout=30):
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
        b = p.chromium.launch(headless=True)
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context()
    page = ctx.new_page()
    yield page
    ctx.close()


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
    page.goto(f"{BASE_URL}/register")

    # Fill separate email and mobile fields
    page.fill("#username", "testuser123")
    page.fill("#email", "test@example.com")
    page.fill("#mobile", "1234567890")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "TestPass123")
    page.fill("#confirm_password", "TestPass123")

    page.click("#registerBtn")

    page.wait_for_selector("#register_message", timeout=5000)
    msg = page.text_content("#register_message") or ""
    assert "Registration successful" in msg


@pytest.mark.e2e
def test_register_password_mismatch(page):
    page.goto(f"{BASE_URL}/register")

    page.fill("#username", "baduser1")
    page.fill("#email", "bad@example.com")
    page.fill("#mobile", "1234567890")
    page.fill("#first_name", "Test")
    page.fill("#last_name", "User")
    page.fill("#password", "Password1")
    page.fill("#confirm_password", "WrongPassword")

    page.click("#registerBtn")

    page.wait_for_selector("#register_message", timeout=5000)
    msg = page.text_content("#register_message") or ""
    assert "match" in msg.lower()


# ----------------------------------------------------------
# LOGIN TESTS (using email_or_mobile field)
# ----------------------------------------------------------
@pytest.mark.e2e
def test_login_positive(page):
    page.goto(f"{BASE_URL}/login")

    page.fill("#email_or_mobile", "test@example.com")
    page.fill("#password", "TestPass123")

    page.click("#loginBtn")

    page.wait_for_selector("#login_message", timeout=5000)
    msg = page.text_content("#login_message") or ""
    assert "Login successful" in msg

    # Token stored
    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is not None
    assert len(token) > 20

    # Dashboard should load
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
