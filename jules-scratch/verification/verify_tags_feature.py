from playwright.sync_api import Page, expect

def test_tags_page_loads(page: Page):
    """
    This test verifies that the tags page loads correctly.
    """
    # 1. Arrange: Go to the tags page.
    page.goto("http://localhost:3001/content/tags")

    # 2. Assert: Check if the main heading is visible.
    heading = page.get_by_role("heading", name="Manage Tags")
    expect(heading).to_be_visible()

    # 3. Screenshot: Capture the page for visual verification.
    page.screenshot(path="jules-scratch/verification/tags_page.png")

    # 4. Act: Click the 'New Tag' button
    new_tag_button = page.get_by_role("link", name="New Tag")
    new_tag_button.click()

    # 5. Assert: Check if the new tag page loads
    expect(page).to_have_url("http://localhost:3001/content/tags/new")
    new_tag_heading = page.get_by_role("heading", name="Create New Tag")
    expect(new_tag_heading).to_be_visible()

    # 6. Act: Fill the form and create a new tag
    tag_name = "Test Tag From Playwright"
    page.get_by_label("Name").fill(tag_name)
    page.get_by_role("button", name="Create Tag").click()

    # 7. Assert: Check if we are redirected to the tags list and the new tag is there
    expect(page).to_have_url("http://localhost:3001/content/tags")
    expect(page.get_by_text(tag_name)).to_be_visible()

    # 8. Screenshot: Capture the page with the new tag
    page.screenshot(path="jules-scratch/verification/tags_page_with_new_tag.png")