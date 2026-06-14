from openai import OpenAI
import json

API_KEY = "2KG3umFrYDIebzGUGsiXPByG0JtcvDZbN2dAshCyTVGbAJuKL8EmJQQJ99CFACHYHv6XJ3w3AAAAACOGJAAH"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://memoryops-iq-resource.services.ai.azure.com/openai/v1"
)

EMBEDDING_MODEL = "text-embedding-3-small"

with open("data/incidents.json", "r") as f:
    incidents = json.load(f)

embedded_incidents = []

for incident in incidents:

    text = f"""
    Service: {incident['service']}
    Region: {incident['region']}
    Severity: {incident['severity']}
    Root Cause: {incident['root_cause']}
    Resolution: {incident['resolution']}
    """

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    embedding = response.data[0].embedding

    embedded_incidents.append({
        "incident": incident,
        "embedding": embedding
    })

    print(f"Embedded {incident['incident_id']}")

with open("data/incident_embeddings.json", "w") as f:
    json.dump(embedded_incidents, f)

print("\nFinished generating embeddings.")
print(f"Total incidents embedded: {len(embedded_incidents)}")