import json
import os

os.makedirs("data/rcas", exist_ok=True)

with open("data/incidents.json", "r") as f:
    incidents = json.load(f)

for incident in incidents:

    rca_text = f"""
ROOT CAUSE ANALYSIS

Incident ID: {incident['incident_id']}

Service:
{incident['service']}

Region:
{incident['region']}

Severity:
{incident['severity']}

Root Cause:
{incident['root_cause']}

Impact:
Service disruption affecting enterprise users.

Resolution:
{incident['resolution']}

MTTR:
{incident['mttr_minutes']} minutes

Lessons Learned:
Additional monitoring and validation should be implemented to reduce recurrence.

Preventive Actions:
1. Improve alerting.
2. Validate changes before deployment.
3. Enhance operational runbooks.
"""

    filename = f"data/rcas/{incident['incident_id']}.txt"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as rca_file:

        rca_file.write(rca_text)

print(
    f"Generated {len(incidents)} RCA files."
)