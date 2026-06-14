import json
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from agents.incident_understanding_agent import classify_incident

with open("evaluations/incident_classification.json", "r") as f:
    test_cases = json.load(f)

passed = 0
total = len(test_cases)

for test in test_cases:
    result = classify_incident(test["input"])
    expected = test["expected"]

    if result == expected:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(f"\n[{status}] Test Case {test['id']}")
    print(f"Input: {test['input']}")
    print(f"Expected: {expected}")
    print(f"Got: {result}")

accuracy = (passed / total) * 100

print("\n========================")
print(f"Passed: {passed}/{total}")
print(f"Accuracy: {accuracy:.2f}%")
print("========================")