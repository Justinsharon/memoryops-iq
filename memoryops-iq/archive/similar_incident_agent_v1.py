import json


def find_similar_incidents(service, region, top_n=3):

    with open("data/incidents.json", "r") as f:
        incidents = json.load(f)

    matches = []

    for incident in incidents:

        score = 0

        if incident["service"] == service:
            score += 2

        if incident["region"] == region:
            score += 1

        if score > 0:
            matches.append(
                {
                    "score": score,
                    "incident": incident
                }
            )

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return [
        m["incident"]
        for m in matches[:top_n]
    ]


if __name__ == "__main__":

    results = find_similar_incidents(
        service="VPN",
        region="APAC"
    )

    print(json.dumps(results, indent=2))