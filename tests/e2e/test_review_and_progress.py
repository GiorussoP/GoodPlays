import pytest


@pytest.mark.e2e
def test_write_review_and_update_progress(page):
    # Log in with existing test user (created during manual testing)
    page.goto('http://127.0.0.1:8000/login')
    page.fill('#username', 'testuser')
    page.fill('#password', 'password123')
    page.click('button[type=submit]')
    page.wait_for_url('**/games')

    # Open a game detail
    page.click('text=View Details')
    page.wait_for_url('**/game/*')

    # Auto-accept alerts that the UI shows
    page.on('dialog', lambda dialog: dialog.accept())

    # Write a review
    page.click('#addReviewBtn')
    # Changed from wait_for_selector to wait_for(state='visible')
    page.wait_for('#addReviewModal', state='visible', timeout=5000)
    page.click('.rating-input .star[data-value="4"]')
    page.fill('#comment', 'Automated e2e review')
    page.click('#submitReviewBtn')
    # wait for the review to appear in the list
    page.wait_for_selector('text=Automated e2e review', timeout=5000)
    assert page.is_visible('text=Automated e2e review')

    # Start/update progress
    # If Start Playing button present, click it; otherwise click Update Progress
    if page.is_visible('text=Start Playing'):
        page.click('text=Start Playing')
    else:
        page.click('text=Update Progress')

    page.wait_for_selector('#progressModal', timeout=5000)
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
    page.wait_for_selector('text=33%', timeout=5000)
    assert page.is_visible('text=33%')
