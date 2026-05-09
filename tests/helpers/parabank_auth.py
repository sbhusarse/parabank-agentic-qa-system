def login_to_parabank(page):
    page.goto("https://parabank.parasoft.com/parabank/index.htm")

    page.fill("input[name='username']", "sbhusarse")
    page.fill("input[name='password']", "Parabank19!")
    page.click("input[value='Log In']")

    page.wait_for_load_state("networkidle")