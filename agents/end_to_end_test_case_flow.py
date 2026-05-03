from test_case_generator import read_requirement, generate_test_cases
from github_issue_creator import create_github_issue


def create_issue_body(test_case_text):
    return f"""
## Source
Sample Requirement: Fund Transfer

## AI Generated Test Case

{test_case_text}

## Review Status
Needs manual review

## Automation Candidate
Yes
"""


if __name__ == "__main__":
    requirement = read_requirement("data/sample_requirement.txt")
    generated_test_cases = generate_test_cases(requirement)

    issue_title = "[AI-TC] Fund Transfer - Generated Test Cases"
    issue_body = create_issue_body(generated_test_cases)
    labels = ["test-case", "ai-generated", "manual-review-needed"]

    create_github_issue(issue_title, issue_body, labels)