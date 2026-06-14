import json
import random

services = {
    "VPN": [
        "Firewall ACL change",
        "VPN Gateway failure",
        "Certificate expiration"
    ],
    "DNS": [
        "DNS zone corruption",
        "DNS server outage",
        "Configuration drift"
    ],
    "BGP": [
        "Route propagation failure",
        "Neighbor flapping",
        "Incorrect route advertisement"
    ],
    "Storage": [
        "Storage account outage",
        "Access key rotation issue",
        "Replication failure"
    ],
    "SQL": [
        "Database deadlock",
        "Connection pool exhaustion",
        "Maintenance window failure"
    ],
    "Key Vault": [
        "RBAC misconfiguration",
        "Secret expiration",
        "Network restriction issue"
    ],
    "App Service": [
        "Deployment failure",
        "Scaling issue",
        "Runtime crash"
    ]
}

regions = [
    "APAC",
    "East US",
    "West Europe",
    "Global"
]

severities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

incidents = []

for i in range(1, 101):

    service = random.choice(list(services.keys()))
    root_cause = random.choice(services[service])

    incident = {
        "incident_id": f"INC-{1000+i}",
        "service": service,
        "region": random.choice(regions),
        "severity": random.choice(severities),
        "root_cause": root_cause,
        "resolution": f"Resolved issue caused by {root_cause}",
        "mttr_minutes": random.randint(15, 180)
    }

    incidents.append(incident)

with open("data/incidents.json", "w") as f:
    json.dump(incidents, f, indent=2)

print(f"Generated {len(incidents)} incidents.")