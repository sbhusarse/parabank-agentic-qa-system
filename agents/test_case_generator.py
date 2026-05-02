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

Generate structured test cases for the requirement below.

Create:
- Positive test cases
- Negative test cases
- Edge test cases

Use this format:

Title:
Type:
Preconditions:
Steps:
Expected Result:

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