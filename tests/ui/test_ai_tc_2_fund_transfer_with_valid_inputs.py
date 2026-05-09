import pytest
from playwright.sync_api import sync_playwright
from helpers.parabank_auth import login_to_parabank

def test_fund_transfer_with_valid_inputs():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Log in to Parabank
        login_to_parabank(page)
        
        # Step 1: Navigate to the Fund Transfer section
        page.click("text='Transfer Funds'")
        
        # Step 2: Select a source account
        page.select_option("select#fromAccountId", "14565")  # Assuming account ID 1 is a valid source
        
        # Step 3: Select a destination account
        page.select_option("select#toAccountId", "14565")  # Assuming account ID 2 is a valid destination
        
        # Step 4: Enter a valid amount
        page.fill("input#amount", "50")  # Assuming 50 is a valid amount
        
        # Step 5: Click on the "Transfer" button
        page.click("input[value='Transfer']")

        # Expected Result: Check for confirmation message
        confirmation_message = page.locator("div#showResult").inner_text()  # Assuming this is the selector for the confirmation message
        assert "Transfer Complete!" in confirmation_message  # Adjust based on actual confirmation text
        
        # Optionally, check account balances if necessary
        # assert page.locator("selector_for_source_balance").inner_text() == "Updated Source Balance"
        # assert page.locator("selector_for_destination_balance").inner_text() == "Updated Destination Balance"
        
        browser.close()