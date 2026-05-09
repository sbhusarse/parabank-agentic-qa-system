import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read_requirement(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def generate_test_cases(requirement_text):
    prompt = f"""
You are a senior QA engineer.

Generate test cases in STRICT structured format.

Each test case must be separated by:

### TEST CASE ###

Format for each test case:

Title:
Type:
Priority:
Preconditions:
Steps:
Expected Result:

Generate at least:
- 2 positive
- 2 negative
- 1 edge case

Requirement:
{requirement_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a QA expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    requirement = read_requirement("data/sample_requirement.txt")
    test_cases = generate_test_cases(requirement)

    print("\nGenerated Test Cases:\n")
    print(test_cases)