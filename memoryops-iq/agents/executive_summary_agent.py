import json

from openai import OpenAI


API_KEY = "2KG3umFrYDIebzGUGsiXPByG0JtcvDZbN2dAshCyTVGbAJuKL8EmJQQJ99CFACHYHv6XJ3w3AAAAACOGJAAH"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://memoryops-iq-resource.services.ai.azure.com/openai/v1"
)

MODEL_NAME = "grok-4-20-reasoning"


def call_grok_text(
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

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
    )


def generate_executive_summary(
    incident_id,
    incident_text,
    classification,
    rca_result,
    remediation_result,
    investigation_result,
    impact_result
):

    prompt = f"""
You are an Executive Incident Manager.

Generate a concise executive summary.

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

Impact:
{json.dumps(impact_result, indent=2)}

Requirements:

1. Business language only.
2. Avoid technical jargon where possible.
3. Maximum 250 words.
4. Cover:

   - Incident Overview
   - Likely Cause
   - Current Status
   - Business Impact
   - Next Steps

Return plain text only.
"""

    return call_grok_text(
        prompt
    )


if __name__ == "__main__":

    print(
        "Executive Summary Agent is a consumer agent and must be called from the orchestrator."
    )