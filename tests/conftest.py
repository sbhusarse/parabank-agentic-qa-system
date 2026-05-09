import os
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page():
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=headless,
            slow_mo=500 if not headless else 0
        )

        context = browser.new_context()
        page = context.new_page()

        yield page

        context.close()
        browser.close()