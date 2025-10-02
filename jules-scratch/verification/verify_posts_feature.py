from playwright.sync_api import sync_playwright, expect
import time

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Go to the app
        page.goto("http://localhost:3000/")

        # Navigate to the Posts page
        page.get_by_role("link", name="Posts").click()

        # Expect the main heading to be visible
        expect(page.get_by_role("heading", name="Manage Posts")).to_be_visible(timeout=10000)

        # Take a screenshot of the initial empty list
        page.screenshot(path="jules-scratch/verification/01_posts_list_empty.png")

        # Go to create a new post
        page.get_by_role("link", name="New Post").click()

        # Expect the heading for the new post page
        expect(page.get_by_role("heading", name="Create New Post")).to_be_visible()

        # Fill out the form
        page.get_by_label("Title").fill("My First Test Post")
        page.get_by_label("Body").fill("This is the body of the test post, created automatically by a script.")

        # Wait for options to be loaded and select the first one for each dropdown
        # A more robust way to wait for options to be populated from API calls
        expect(page.locator("#campaign > option:nth-child(2)")).to_be_enabled(timeout=10000)
        page.get_by_label("Campaign").select_option(index=1)

        expect(page.locator("#platform > option:nth-child(2)")).to_be_enabled()
        page.get_by_label("Platform").select_option(index=1)

        expect(page.locator("#postType > option:nth-child(2)")).to_be_enabled()
        page.get_by_label("Post Type").select_option(index=1)

        expect(page.locator("#status > option:nth-child(2)")).to_be_enabled()
        page.get_by_label("Status").select_option(index=1)

        # Submit the form
        page.get_by_role("button", name="Create Post").click()

        # Wait for the URL to change back to the posts list
        page.wait_for_url("http://localhost:3000/content/posts", timeout=10000)

        # Now that we are on the correct page, check for the heading and the success message
        expect(page.get_by_role("heading", name="Manage Posts")).to_be_visible()
        expect(page.get_by_text("Post created successfully!")).to_be_visible()

        # Wait for the new post to appear in the table
        expect(page.get_by_role("cell", name="My First Test Post")).to_be_visible()

        # Take the final screenshot
        page.screenshot(path="jules-scratch/verification/02_posts_list_with_item.png")
        print("Verification script completed successfully!")

    except Exception as e:
        print(f"An error occurred during verification: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")
    finally:
        # Clean up
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)