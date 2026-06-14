import os
import sys
import json
import re
from datetime import datetime

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


def get_inline_field(
    text,
    field
):

    pattern = (
        rf"^{re.escape(field)}:\s*(.*)$"
    )

    match = re.search(
        pattern,
        text,
        re.MULTILINE
    )

    if match:
        return match.group(1).strip()

    return ""


def get_block_field(
    text,
    field
):

    pattern = (
        rf"^{re.escape(field)}:\s*\n(.*?)(?:\n\n|\Z)"
    )

    match = re.search(
        pattern,
        text,
        re.MULTILINE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def calculate_score(
    classification,
    change
):

    score = 0

    reasons = []

    #
    # HARD GATE
    #

    if (
        change["service"].lower()
        !=
        classification["service"].lower()
    ):

        return 0, [
            "Service mismatch"
        ]

    score += 40

    reasons.append(
        "Service matched"
    )

    #
    # Region
    #

    if (
        change["region"].lower()
        ==
        classification["region"].lower()
    ):

        score += 20

        reasons.append(
            "Region matched"
        )

    elif (
        change["region"].lower()
        ==
        "global"
    ):

        score += 10

        reasons.append(
            "Global change"
        )

    #
    # Time Window
    #

    try:

        change_time = datetime.strptime(
            change["start_time"],
            "%Y-%m-%d %H:%M:%S"
        )

        age_hours = (
            datetime.now()
            - change_time
        ).total_seconds() / 3600

        if age_hours <= 24:

            score += 20

            reasons.append(
                "Change within 24 hours"
            )

        elif age_hours <= 72:

            score += 15

            reasons.append(
                "Change within 72 hours"
            )

    except:

        pass

    #
    # Status
    #

    status = (
        change["status"]
        .lower()
    )

    if status == "failed":

        score += 20

        reasons.append(
            "Change failed"
        )

    elif status == "rolled back":

        score += 20

        reasons.append(
            "Change rolled back"
        )

    elif status == "partially successful":

        score += 10

        reasons.append(
            "Partially successful change"
        )

    #
    # Validation
    #

    validation = (
        change["validation"]
        .lower()
    )

    if validation == "failed":

        score += 15

        reasons.append(
            "Validation failed"
        )

    elif (
        validation
        ==
        "passed with warnings"
    ):

        score += 10

        reasons.append(
            "Validation warnings"
        )

    return score, reasons


def find_correlated_change(
    incident_text,
	classification
):


    changes = []

    for filename in os.listdir(
        "data/changes"
    ):

        if not filename.endswith(
            ".txt"
        ):
            continue

        path = os.path.join(
            "data/changes",
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        change = {

            "change_id":
                get_inline_field(
                    content,
                    "Change ID"
                ),

            "service":
                get_block_field(
                    content,
                    "Service"
                ),

            "region":
                get_block_field(
                    content,
                    "Region"
                ),

            "change_type":
                get_block_field(
                    content,
                    "Change Type"
                ),

            "risk":
                get_block_field(
                    content,
                    "Risk Level"
                ),

            "start_time":
                get_block_field(
                    content,
                    "Change Start"
                ),

            "validation":
                get_block_field(
                    content,
                    "Validation Result"
                ),

            "status":
                get_block_field(
                    content,
                    "Status"
                )
        }

        score, reasons = (
            calculate_score(
                classification,
                change
            )
        )

        change["score"] = score

        change["reasons"] = reasons

        changes.append(
            change
        )

    changes.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    if not changes:

        return {
            "change_found": False,
            "correlation": "LOW",
            "confidence": 0
        }

    best = changes[0]

    #
    # Enterprise Threshold
    #

    if best["score"] < 70:

        return {

            "change_found":
                False,

            "correlation":
                "LOW",

            "confidence":
                best["score"],

            "reason":
                "No sufficiently correlated change identified"
        }

    return {

        "change_found":
            True,

        "change_id":
            best["change_id"],

        "service":
            best["service"],

        "region":
            best["region"],

        "change_type":
            best["change_type"],

        "status":
            best["status"],

        "validation":
            best["validation"],

        "correlation":
            "HIGH",

        "confidence":
            best["score"],

        "correlation_reason":
            ", ".join(
                best["reasons"]
            )
    }


if __name__ == "__main__":

    incident = input(
        "Enter incident description: "
    )

    result = (
        find_correlated_change(
            incident
        )
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )