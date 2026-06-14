import json

from openai import OpenAI


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


def generate_impact(
    incident_id,
    incident_text,
    classification,
    rca_result,
    remediation_result,
    investigation_result
):

    prompt = f"""
You are a Senior Enterprise Incident Manager.

Incident ID:
{incident_id}

Incident:
{incident_text}

Classification:
{json.dumps(classification, indent=2)}

RCA:
{json.dumps(rca_result, indent=2)}

Remediation:
{json.dumps(remediation_result, indent=2)}

Investigation:
{json.dumps(investigation_result, indent=2)}

Estimate:

1. Users affected
2. Business impact
3. MTTR improvement achievable using MemoryOps IQ
4. Potential downtime remaining
5. Reasoning

Return JSON only.

{{
    "users_affected": 0,
    "business_impact": "",
    "mttr_improvement": "",
    "potential_downtime": "",
    "reasoning": ""
}}
"""

    return call_grok_json(
        prompt
    )


if __name__ == "__main__":

    print(
        json.dumps(
            {
                "message":
                    (
                        "Impact Agent is now a "
                        "consumer agent and "
                        "must be called from "
                        "the orchestrator."
                    )
            },
            indent=2
        )
    )