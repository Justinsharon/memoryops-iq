import json
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from agents.gpt_incident_agent import classify_incident

with open("evaluations/gold_incident_dataset.json", "r") as f:
    tests = json.load(f)

passed = 0

for test in tests:

    result = classify_incident(test["input"])
    expected = test["expected"]

    service_match = (
        result["service"].lower()
        == expected["service"].lower()
    )

    region_match = (
        result["region"].lower()
        == expected["region"].lower()
    )

    category_match = (
        result["category"].lower()
        == expected["category"].lower()
    )

    if service_match and region_match and category_match:
        passed += 1
    else:

        print("\n--------------------------------")
        print("FAIL")

        print("INPUT:")
        print(test["input"])

        print("\nEXPECTED:")
        print(expected)

        print("\nGOT:")
        print(result)

accuracy = (passed / len(tests)) * 100

print("\n========================")
print(f"Passed: {passed}/{len(tests)}")
print(f"Accuracy: {accuracy:.2f}%")
print("========================")