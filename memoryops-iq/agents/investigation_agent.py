import os
import sys
import json

from openai import OpenAI

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)



API_KEY = "2KG3umFrYDIebzGUGsiXPByG0JtcvDZbN2dAshCyTVGbAJuKL8EmJQQJ99CFACHYHv6XJ3w3AAAAACOGJAAH"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://memoryops-iq-resource.services.ai.azure.com/openai/v1"
)

MODEL_NAME = "grok-4-20-reasoning"


def call_grok_json(
    prompt
):

    response = (
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    return json.loads(
        content
    )


def generate_investigation(
    incident_text,
    remediation_result
):

    prompt = f"""
You are a Senior Enterprise Incident Investigator.

Incident:
{incident_text}

Service:
{remediation_result.get("service")}

Primary Hypothesis:
{remediation_result.get("primary_hypothesis")}

Alternative Hypothesis:
{remediation_result.get("alternative_hypothesis")}

Actions Attempted:
{json.dumps(remediation_result.get("recommended_actions", []), indent=2)}

Investigation Status:
Issue Persists

The remediation actions were executed but the issue still exists.

Assume the original hypothesis may be incomplete or incorrect.

Generate:

1. New hypotheses
2. Additional checks
3. Deep-dive investigation steps
4. Escalation recommendation
5. Reasoning

Return JSON only.

{{
    "new_hypotheses": [],
    "additional_checks": [],
    "deep_dive_steps": [],
    "escalation_recommendation": "",
    "reasoning": ""
}}
"""

    return call_grok_json(
        prompt
    )


def investigate_incident(
    incident_text,
    remediation_result
):

    investigation = (
        generate_investigation(
            incident_text,
            remediation_result
        )
    )

    return {

        "investigation_trigger":
            "Remediation Failed",

        "investigation_status":
            "Issue Persists",

        "escalation_level":
            "Tier 3",

        "service":
            remediation_result.get(
                "service"
            ),

        "primary_hypothesis":
            remediation_result.get(
                "primary_hypothesis"
            ),

        "alternative_hypothesis":
            remediation_result.get(
                "alternative_hypothesis"
            ),

        "actions_attempted":
            remediation_result.get(
                "recommended_actions",
                []
            ),

        "new_hypotheses":
            investigation.get(
                "new_hypotheses",
                []
            ),

        "additional_checks":
            investigation.get(
                "additional_checks",
                []
            ),

        "deep_dive_steps":
            investigation.get(
                "deep_dive_steps",
                []
            ),

        "escalation_recommendation":
            investigation.get(
                "escalation_recommendation",
                ""
            ),

        "reasoning":
            investigation.get(
                "reasoning",
                ""
            )
    }


if __name__ == "__main__":

    incident = input(
        "Enter incident description: "
    )

    result = (
        investigate_incident(
            incident
        )
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )