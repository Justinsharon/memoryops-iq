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


def extract_runbook_steps(
    runbook_text
):

    steps = []

    for line in runbook_text.splitlines():

        line = line.strip()

        if (
            line.startswith("1.")
            or line.startswith("2.")
            or line.startswith("3.")
            or line.startswith("4.")
            or line.startswith("5.")
            or line.startswith("6.")
            or line.startswith("7.")
            or line.startswith("8.")
        ):

            steps.append(line)

    return steps


def determine_service_from_rca(
    rca_result
):

    service = (
        rca_result.get(
            "service"
        )
    )

    if service:

        return service

    return "Unknown"


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


def generate_runbook_enhancement(
    incident_text,
    classification,
    rca_result,
    grounded_actions
):

    prompt = f"""
You are a Senior Enterprise Incident Response Engineer.

Incident:
{incident_text}

Classification:
{json.dumps(classification, indent=2)}

Historical Match Found:
{rca_result.get("historical_match_found")}

Primary Hypothesis:
{rca_result.get("primary_hypothesis")}

Alternative Hypothesis:
{rca_result.get("alternative_hypothesis")}

Change Found:
{rca_result.get("change_found")}

Change Type:
{rca_result.get("change_type")}

Change ID:
{rca_result.get("change_id")}

RCA Reasoning:
{rca_result.get("reasoning")}

Grounded Actions:
{json.dumps(grounded_actions, indent=2)}

RULES:

1. NEVER remove runbook actions.
2. NEVER rewrite runbook actions.
3. ONLY add actions.
4. Add validation steps.
5. Add escalation guidance.
6. Stay grounded in evidence.
7. Return JSON only.

Return:

{{
  "recommended_actions": [],
  "validation_steps": [],
  "escalation_guidance": "",
  "reasoning": ""
}}
"""

    return call_grok_json(
        prompt
    )


def generate_ai_plan(
    incident_text,
    classification,
    rca_result,
    service
):

    prompt = f"""
You are a Senior Enterprise Incident Response Engineer.

Incident:
{incident_text}

Classification:
{json.dumps(classification, indent=2)}

Service:
{service}

Historical Match Found:
{rca_result.get("historical_match_found")}

Primary Hypothesis:
{rca_result.get("primary_hypothesis")}

Alternative Hypothesis:
{rca_result.get("alternative_hypothesis")}

Change Found:
{rca_result.get("change_found")}

Change Type:
{rca_result.get("change_type")}

Change ID:
{rca_result.get("change_id")}

RCA Reasoning:
{rca_result.get("reasoning")}

No runbook exists.

Generate a complete remediation plan.

Requirements:

- Troubleshooting actions
- Validation steps
- Escalation guidance
- Reasoning

Return JSON only.

Return:

{{
  "recommended_actions": [],
  "validation_steps": [],
  "escalation_guidance": "",
  "reasoning": ""
}}
"""

    return call_grok_json(
        prompt
    )


def recommend_remediation(
    incident_text,
    classification,
    rca_result
):

    service = (
        determine_service_from_rca(
           rca_result
        )
    )

    runbook_map = {

        "VPN":
            "data/runbooks/vpn_runbook.txt",

        "DNS":
            "data/runbooks/dns_runbook.txt",

        "SQL":
            "data/runbooks/sql_runbook.txt",

        "Storage":
            "data/runbooks/storage_runbook.txt",

        "Key Vault":
            "data/runbooks/key vault_runbook.txt",

        "App Service":
            "data/runbooks/app service_runbook.txt",

        "Routing":
            "data/runbooks/bgp_runbook.txt"
    }

    runbook_path = (
        runbook_map.get(
            service
        )
    )

    if (
        runbook_path
        and
        os.path.exists(
            runbook_path
        )
    ):

        with open(
            runbook_path,
            "r",
            encoding="utf-8"
        ) as f:

            runbook_text = f.read()

        grounded_actions = (
            extract_runbook_steps(
                runbook_text
            )
        )

        if (
            rca_result.get(
                "change_found"
            )
        ):

            change_id = (
                rca_result.get(
                    "change_id"
                )
            )

            grounded_actions.insert(
                0,
                f"Review change record {change_id}"
            )

            grounded_actions.insert(
                1,
                "Validate rollback status and post-change validation"
            )

        ai_output = (
            generate_runbook_enhancement(
                incident_text,
                classification,
                rca_result,
                grounded_actions
            )
        )

        combined_actions = (
            grounded_actions
            +
            ai_output.get(
                "recommended_actions",
                []
            )
        )

        combined_actions = list(
            dict.fromkeys(
                combined_actions
            )
        )

        return {

            "execution_status":
                "Not Started",

            "service":
                service,

            "source":
                "runbook_enhanced",

            "historical_match_found":
                rca_result.get(
                    "historical_match_found"
                ),

            "change_found":
                rca_result.get(
                    "change_found"
                ),

            "primary_hypothesis":
                rca_result.get(
                    "primary_hypothesis"
                ),

            "alternative_hypothesis":
                rca_result.get(
                    "alternative_hypothesis"
                ),

            "recommended_actions":
                combined_actions,

            "validation_steps":
                ai_output.get(
                    "validation_steps",
                    []
                ),

            "escalation_guidance":
                ai_output.get(
                    "escalation_guidance",
                    ""
                ),

            "reasoning":
                ai_output.get(
                    "reasoning",
                    ""
                )
        }

    ai_output = (
        generate_ai_plan(
            incident_text,
            classification,
            rca_result,
            service
        )
    )

    return {

        "execution_status":
            "Not Started",

        "service":
            service,

        "source":
            "ai_generated",

        "historical_match_found":
            rca_result.get(
                "historical_match_found"
            ),

        "change_found":
            rca_result.get(
                "change_found"
            ),

        "primary_hypothesis":
            rca_result.get(
                "primary_hypothesis"
            ),

        "alternative_hypothesis":
            rca_result.get(
                "alternative_hypothesis"
            ),

        "recommended_actions":
            ai_output.get(
                "recommended_actions",
                []
            ),

        "validation_steps":
            ai_output.get(
                "validation_steps",
                []
            ),

        "escalation_guidance":
            ai_output.get(
                "escalation_guidance",
                ""
            ),

        "reasoning":
            ai_output.get(
                "reasoning",
                ""
            )
    }


if __name__ == "__main__":

    print(
        json.dumps(
            {
                "message":
                    (
                        "Remediation Agent is now a "
                        "consumer agent and must be "
                        "called from the orchestrator."
                    )
            },
            indent=2
        )
    )