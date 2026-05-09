from agents.test_case_generator import read_requirement, generate_test_cases
from agents.github_issue_creator import create_github_issue


def split_test_cases(generated_text):
    return generated_text.split("### TEST CASE ###")


def extract_title(test_case_text, index):
    for line in test_case_text.splitlines():
        if line.strip().startswith("Title:"):
            title = line.replace("Title:", "").strip()
            if title:
                return f"[AI-TC-{index}] {title}"

    return f"[AI-TC-{index}] Parabank Fund Transfer Test Case"


def create_issue_body(test_case_text):
    return f"""
## AI Generated Test Case

{test_case_text.strip()}

## Review Status
Needs manual review

## Automation Candidate
Yes
"""


if __name__ == "__main__":
    requirement = read_requirement("data/sample_requirement.txt")
    generated_text = generate_test_cases(requirement)

    test_cases = split_test_cases(generated_text)

    issue_count = 0

    for test_case in test_cases:
        if test_case.strip():
            issue_count += 1
            issue_title = extract_title(test_case, issue_count)
            issue_body = create_issue_body(test_case)

            create_github_issue(
                issue_title,
                issue_body,
                ["test-case", "ai-generated", "manual-review-needed"]
            )

    print(f"\nTotal GitHub issues created: {issue_count}")