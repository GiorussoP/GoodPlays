import pytest

import pytest


@pytest.mark.e2e
def test_write_review_and_update_progress(page):
    # Register a new test user
    page.goto('http://127.0.0.1:8000/register')
    page.fill('#username', 'testuser')
    page.fill('#email', 'testuser@example.com')
    page.fill('#password', 'password123')
    page.click('button[type=submit]')
    page.wait_for_url('**/login')
    
    # Log in with the newly created user
    page.fill('#username', 'testuser')
    page.fill('#password', 'password123')
    page.click('button[type=submit]')
    page.wait_for_url('**/games')

    # Wait for games to load and then open a game detail
    page.wait_for_selector('.game-card', timeout=10000)
    page.click('a:has-text("View Details")')
    page.wait_for_url('**/game/*')

    # Auto-accept alerts that the UI shows
    page.on('dialog', lambda dialog: dialog.accept())

    # Write a review
    page.click('#addReviewBtn')
    # Wait for the modal to be visible
    page.wait_for_selector('#addReviewModal', state='visible', timeout=10000)
    page.click('.rating-input .star[data-value="4"]')
    page.fill('#comment', 'Automated e2e review')
    page.click('#submitReviewBtn')
    # wait for the review to appear in the list
    page.wait_for_selector('text=Automated e2e review', timeout=10000)
    assert page.is_visible('text=Automated e2e review')

    # Start/update progress
    # If Start Playing button present, click it; otherwise click Update Progress
    if page.is_visible('text=Start Playing'):
        page.click('text=Start Playing')
    else:
        page.click('text=Update Progress')

    page.wait_for_selector('#progressModal', state='visible', timeout=10000)
    # set slider value via JS and set a last played date
    page.evaluate("""
        () => {
            document.getElementById('progressPercentage').value = 33;
            document.getElementById('progressPercentageDisplay').textContent = '33';
            const dt = new Date(); dt.setHours(dt.getHours()-1);
            document.getElementById('lastPlayed').value = dt.toISOString().slice(0,16);
        }
    """)
    page.click('#submitProgressBtn')
    # confirm progress updated in UI
    page.wait_for_selector('text=33%', timeout=10000)
    assert page.is_visible('text=33%')

