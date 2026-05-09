import os
import re
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")

READY_LABEL = "ready-for-automation"
GENERATED_LABEL = "automation-generated"
FAILED_LABEL = "automation-failed"


def github_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def fetch_ready_issues():
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues"
    params = {
        "labels": READY_LABEL,
        "state": "open",
    }

    response = requests.get(url, headers=github_headers(), params=params)

    if response.status_code == 200:
        return response.json()

    print("Failed to fetch ready issues")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    return []


def generate_playwright_test(test_case_text):
    prompt = f"""
You are a QA Automation Engineer.

Convert the following test case into a Playwright Python test using pytest.

Requirements:
- Return only raw Python code
- Do not include markdown
- Do not include ```python
- Use Playwright Python sync API
- Use pytest
- Use page.goto()
- Include assertions
- Use clear selectors and comments if selectors are assumed
- Every test must import and use:
  from helpers.parabank_auth import login_to_parabank
- Every test must call login_to_parabank(page) before testing authenticated Parabank flows
- Do not generate login steps manually

Test Case:
{test_case_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate clean Playwright Python automation code."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def clean_generated_code(code):
    code = code.strip()

    if code.startswith("```python"):
        code = code.replace("```python", "", 1).strip()

    if code.startswith("```"):
        code = code.replace("```", "", 1).strip()

    if code.endswith("```"):
        code = code[:-3].strip()

    return code


def sanitize_filename(title):
    safe_name = title.lower()
    safe_name = re.sub(r"[^a-z0-9]+", "_", safe_name)
    return safe_name.strip("_")


def save_test_file(issue_title, code):
    os.makedirs("tests/ui", exist_ok=True)

    clean_code = clean_generated_code(code)
    safe_name = sanitize_filename(issue_title)

    file_path = f"tests/ui/test_{safe_name}.py"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(clean_code)

    print(f"Saved file: {file_path}")


def update_issue_labels(issue_number, labels_to_add, labels_to_remove):
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/issues/{issue_number}"

    get_response = requests.get(url, headers=github_headers())

    if get_response.status_code != 200:
        print(f"Failed to read issue #{issue_number}")
        return

    issue = get_response.json()
    existing_labels = [label["name"] for label in issue.get("labels", [])]

    final_labels = set(existing_labels)

    for label in labels_to_add:
        final_labels.add(label)

    for label in labels_to_remove:
        final_labels.discard(label)

    patch_response = requests.patch(
        url,
        headers=github_headers(),
        json={"labels": list(final_labels)},
    )

    if patch_response.status_code == 200:
        print(f"Updated labels for issue #{issue_number}")
    else:
        print(f"Failed to update labels for issue #{issue_number}")
        print(patch_response.text)


if __name__ == "__main__":
    ready_issues = fetch_ready_issues()

    if not ready_issues:
        print("No issues found with label: ready-for-automation")

    for issue in ready_issues:
        try:
            issue_number = issue["number"]
            issue_title = issue["title"]
            issue_body = issue.get("body", "")

            print(f"Generating automation for issue #{issue_number}: {issue_title}")

            test_code = generate_playwright_test(issue_body)
            save_test_file(issue_title, test_code)

            update_issue_labels(
                issue_number,
                labels_to_add=[GENERATED_LABEL],
                labels_to_remove=[READY_LABEL, FAILED_LABEL],
            )

        except Exception as error:
            print(f"Automation generation failed for issue #{issue.get('number')}")
            print(error)

            update_issue_labels(
                issue["number"],
                labels_to_add=[FAILED_LABEL],
                labels_to_remove=[READY_LABEL],
            )