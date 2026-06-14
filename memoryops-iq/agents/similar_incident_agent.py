import os
import sys
import json
import math

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from openai import OpenAI
from agents.gpt_incident_agent import classify_incident

API_KEY = "2KG3umFrYDIebzGUGsiXPByG0JtcvDZbN2dAshCyTVGbAJuKL8EmJQQJ99CFACHYHv6XJ3w3AAAAACOGJAAH"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://memoryops-iq-resource.services.ai.azure.com/openai/v1"
)

EMBEDDING_MODEL = "text-embedding-3-small"


def cosine_similarity(
    vec1,
    vec2
):

    dot_product = sum(
        a * b
        for a, b in zip(
            vec1,
            vec2
        )
    )

    magnitude1 = math.sqrt(
        sum(
            a * a
            for a in vec1
        )
    )

    magnitude2 = math.sqrt(
        sum(
            b * b
            for b in vec2
        )
    )

    if (
        magnitude1 == 0
        or
        magnitude2 == 0
    ):
        return 0

    return (
        dot_product
        /
        (
            magnitude1
            *
            magnitude2
        )
    )


def find_similar_incidents(
    incident_text,
	classification,
    top_k=5
):


    query_text = f"""
Service: {classification['service']}
Region: {classification['region']}
Category: {classification['category']}
Incident: {incident_text}
"""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query_text
    )

    query_embedding = (
        response.data[0].embedding
    )

    with open(
        "data/incident_embeddings.json",
        "r",
        encoding="utf-8"
    ) as f:

        embedded_incidents = (
            json.load(f)
        )

    scored_results = []

    for item in embedded_incidents:

        incident = item["incident"]

        similarity = (
            cosine_similarity(
                query_embedding,
                item["embedding"]
            )
        )

        score = similarity

        #
        # Service Boost
        #

        if (
            incident["service"]
            ==
            classification["service"]
        ):

            score += 0.20

        #
        # Region Boost
        #

        if (
            incident["region"]
            ==
            classification["region"]
        ):

            score += 0.10

        scored_results.append(
            {
                "score": round(
                    score,
                    4
                ),
                "incident": incident
            }
        )

    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_results[:top_k]


def find_best_match(
    incident_text,
	classification,
    threshold=0.90
):

    matches = (
        find_similar_incidents(
            incident_text,
			classification,
            top_k=1
        )
    )

    if not matches:

        return None

    best_match = matches[0]

    if (
        best_match["score"]
        <
        threshold
    ):

        return None

    return best_match


if __name__ == "__main__":

    incident = input(
        "Enter incident description: "
    )

    results = (
        find_similar_incidents(
            incident
        )
    )

    print("\nTOP MATCHES\n")

    for result in results:

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        print()

    print(
        "\nBEST MATCH CHECK\n"
    )

    best = (
        find_best_match(
            incident
        )
    )

    if best:

        print(
            json.dumps(
                best,
                indent=2
            )
        )

    else:

        print(
            "No sufficiently similar historical incident found."
        )