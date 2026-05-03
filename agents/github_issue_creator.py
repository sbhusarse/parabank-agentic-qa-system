import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")


def create_github_issue(title, body, labels):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    payload = {
        "title": title,
        "body": body,
        "labels": labels,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("GitHub issue created successfully.")
        print(response.json()["html_url"])
    else:
        print("Failed to create GitHub issue.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    issue_title = "[TC] Verify successful fund transfer with valid inputs"

    issue_body = """
## Source
Manual Sample Requirement

## Test Type
Positive Functional Test

## Preconditions
- User is registered
- User is logged in
- User has at least two accounts
- Source account has sufficient balance

## Test Steps
1. Navigate to Transfer Funds page
2. Select source account
3. Select destination account
4. Enter valid transfer amount
5. Click Transfer

## Expected Result
Funds should be transferred successfully and confirmation message should be displayed.

## Automation Candidate
Yes

## Priority
High
"""

    labels = ["test-case", "ui", "functional", "automation-candidate"]

    create_github_issue(issue_title, issue_body, labels)