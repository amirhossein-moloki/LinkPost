import re
from playwright.sync_api import Page, expect, sync_playwright

def verify_frontend(page: Page):
    """
    This script verifies the new UI for the campaign management pages.
    It captures screenshots of the list, new, and edit pages.
    """

    # 1. Navigate to the campaign list and verify the new table
    print("Navigating to Campaigns page...")
    page.goto("http://localhost:3000/content/campaigns")

    # Wait for the heading to be visible and assert its content
    heading = page.get_by_role("heading", name="Manage Campaigns")
    expect(heading).to_be_visible(timeout=10000)

    # Verify the new "New Campaign" button is there
    new_campaign_button = page.get_by_role("link", name="New Campaign")
    expect(new_campaign_button).to_be_visible()

    # Wait for the table to load data. We check for the table body.
    table_body = page.locator("tbody")
    expect(table_body).to_be_visible()

    print("Capturing screenshot of the Campaigns List page...")
    page.screenshot(path="jules-scratch/verification/01_campaigns_list.png")

    # 2. Verify the "New Campaign" page
    print("Navigating to New Campaign page...")
    new_campaign_button.click()

    # Wait for the new campaign page to load and verify its title
    new_heading = page.get_by_role("heading", name="Create New Campaign")
    expect(new_heading).to_be_visible()

    # Check for the new input fields
    expect(page.get_by_label("Campaign Name")).to_be_visible()
    expect(page.get_by_label("Description")).to_be_visible()

    print("Capturing screenshot of the New Campaign page...")
    page.screenshot(path="jules-scratch/verification/02_new_campaign.png")

    # 3. Verify the "Edit Campaign" page
    print("Navigating back to list to test Edit page...")
    page.get_by_role("link", name="Cancel").click()
    expect(heading).to_be_visible() # Wait for list page to load

    # Find the first row's action menu and click it
    # Note: This assumes at least one campaign exists.
    # If not, this part would fail, which is acceptable for this verification.
    first_row_actions = page.locator('tbody tr:first-child button[aria-haspopup="menu"]')

    if first_row_actions.count() > 0:
        first_row_actions.click()

        # Click the "Edit" link in the dropdown
        edit_link = page.get_by_role("menuitem", name="Edit")
        edit_link.click()

        # Wait for the edit page to load
        edit_heading = page.get_by_role("heading", name="Edit Campaign")
        expect(edit_heading).to_be_visible()

        # Check if the form fields are populated (have a non-empty value)
        expect(page.get_by_label("Campaign Name")).not_to_be_empty()
        expect(page.get_by_label("Description")).not_to_be_empty()

        print("Capturing screenshot of the Edit Campaign page...")
        page.screenshot(path="jules-scratch/verification/03_edit_campaign.png")
    else:
        print("Skipping Edit page verification as no campaigns were found.")


def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        verify_frontend(page)
        browser.close()

if __name__ == "__main__":
    run_verification()