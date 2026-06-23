import time
import pytest


@pytest.mark.e2e
def test_register_login_and_browse_games(page):
    # Use a timestamped username to avoid collisions
    username = f"e2e_user_{int(time.time())}"
    password = "password123"

    # Register
    page.goto("http://127.0.0.1:8000/register")
    page.fill('#username', username)
    page.fill('#email', f"{username}@example.com")
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type=submit]')
    # wait for redirect to login
    page.wait_for_url("**/login*")

    # Login
    page.fill('#username', username)
    page.fill('#password', password)
    page.click('button[type=submit]')
    page.wait_for_url("**/games")

    # Verify games list is visible
    assert page.is_visible('text=Browse Games')
    # Ensure at least one game card exists
    page.wait_for_selector('text=View Details')
    assert page.locator('text=View Details').nth(0).is_visible()
