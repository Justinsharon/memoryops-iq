import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.gpt_incident_agent import classify_incident

with open("evaluations/incident_classification.json", "r") as f:
    test_cases = json.load(f)

passed = 0
total = len(test_cases)

for test in test_cases:

    result = classify_incident(test["input"])

    expected = test["expected"]

    if (
        result["service"].lower() == expected["service"].lower()
        and result["region"].lower() == expected["region"].lower()
        and result["category"].lower() == expected["category"].lower()
    ):
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(f"\n[{status}] Test Case {test['id']}")
    print("Input:", test["input"])
    print("Expected:", expected)
    print("Got:", result)

accuracy = (passed / total) * 100

print("\n========================")
print(f"Passed: {passed}/{total}")
print(f"Accuracy: {accuracy:.2f}%")
print("========================")