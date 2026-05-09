import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_latest_report():
    report_dir = Path("reports/execution")
    reports = list(report_dir.glob("test_run_*.txt"))

    if not reports:
        raise FileNotFoundError("No execution reports found in reports/execution")

    return max(reports, key=lambda file: file.stat().st_mtime)


def read_report(report_path):
    with open(report_path, "r", encoding="utf-8") as file:
        return file.read()


def analyze_report(report_content):
    prompt = f"""
You are a senior QA automation lead.

Analyze the following pytest execution report.

Provide:
1. Test execution summary
2. Passed/failed count
3. Failure root cause
4. Whether failure appears to be application issue, test script issue, selector issue, data issue, or environment issue
5. Recommended next action

Keep the answer clear and practical.

Pytest Report:
{report_content}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze QA automation test execution reports."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def save_analysis(analysis_text):
    os.makedirs("reports/analysis", exist_ok=True)

    output_path = "reports/analysis/latest_analysis.txt"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(analysis_text)

    print(f"Analysis saved at: {output_path}")


if __name__ == "__main__":
    latest_report = get_latest_report()
    print(f"Analyzing report: {latest_report}")

    report_content = read_report(latest_report)
    analysis = analyze_report(report_content)

    print("\n=== TEST ANALYSIS ===\n")
    print(analysis)

    save_analysis(analysis)