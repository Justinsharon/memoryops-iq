import json

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


PROJECT_ENDPOINT = (
    "https://memoryops-iq-resource.services.ai.azure.com/api/projects/memoryops-iq"
)

AGENT_NAME = "memoryopsIQ"
AGENT_VERSION = "7"


project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

openai_client = (
    project_client.get_openai_client()
)


def retrieve_foundry_context(
    incident_text
):

    prompt = f"""
Incident:

{incident_text}

Return only JSON using the structure defined in your instructions.
Do not return markdown.
Do not return explanations.
"""

    response = (
        openai_client.responses.create(
            input=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            extra_body={
                "agent_reference": {
                    "name": AGENT_NAME,
                    "version": AGENT_VERSION,
                    "type": "agent_reference"
                }
            }
        )
    )

    raw_text = (
        response.output_text
        .strip()
    )

    try:

        if raw_text.startswith("```json"):

            raw_text = (
                raw_text
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

        result = (
            json.loads(
                raw_text
            )
        )

        return result

    except Exception as e:

        print(
            "\nJSON PARSE FAILED\n"
        )

        print(
            str(e)
        )

        return {
            "similar_incidents": [],
            "related_change_records": [],
            "runbooks": [],
            "likely_root_causes": [],
            "evidence": []
        }


if __name__ == "__main__":

    result = (
        retrieve_foundry_context(
            "DNS resolution failures across APAC after DNS configuration update"
        )
    )

    print(
        "\nPARSED RESULT\n"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )