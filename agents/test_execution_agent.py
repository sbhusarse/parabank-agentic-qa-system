import os
import subprocess
from datetime import datetime


def run_tests():
    os.makedirs("reports/execution", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/execution/test_run_{timestamp}.txt"

    command = ["pytest", "tests/ui", "-v"]

    with open(report_file, "w", encoding="utf-8") as file:
        result = subprocess.run(
            command,
            stdout=file,
            stderr=subprocess.STDOUT,
            text=True
        )

    print(f"Test execution completed.")
    print(f"Report saved at: {report_file}")
    print(f"Exit code: {result.returncode}")

    return result.returncode, report_file


if __name__ == "__main__":
    run_tests()