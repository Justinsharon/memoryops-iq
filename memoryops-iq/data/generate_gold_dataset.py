import json
import random

services = [
    ("VPN", "Network"),
    ("DNS", "Network"),
    ("Firewall", "Network"),
    ("Routing", "Network"),
    ("Identity", "Security"),
    ("Certificate", "Security"),
    ("Key Vault", "Security"),
    ("Storage", "Cloud"),
    ("SQL", "Cloud"),
    ("App Service", "Cloud")
]

regions = [
    "APAC",
    "East US",
    "West Europe",
    "Global"
]

templates = {
    "VPN": [
        "VPN outage affecting users in {region}",
        "Remote users unable to connect via VPN in {region}"
    ],

    "DNS": [
        "DNS resolution failures impacting applications in {region}",
        "Customers reporting DNS lookup failures in {region}"
    ],

    "Firewall": [
        "Firewall ACL update blocking traffic in {region}",
        "Firewall policy change causing connectivity issues in {region}"
    ],

    "Routing": [
        "BGP route instability impacting connectivity in {region}",
        "Routing issues detected across network backbone in {region}"
    ],

    "Identity": [
        "Users unable to authenticate after policy update in {region}",
        "MFA failures impacting user sign in across {region}"
    ],

    "Certificate": [
        "Certificate expired causing HTTPS failures in {region}",
        "SSL certificate issue impacting applications in {region}"
    ],

    "Key Vault": [
        "Key Vault access denied after RBAC modification in {region}",
        "Applications unable to retrieve secrets from Key Vault in {region}"
    ],

    "Storage": [
        "Azure Storage account unavailable in {region}",
        "Blob storage access failures reported in {region}"
    ],

    "SQL": [
        "Azure SQL database unavailable in {region}",
        "SQL connections timing out in {region}"
    ],

    "App Service": [
        "App Service deployment failed after pipeline update in {region}",
        "Application deployment failure in App Service in {region}"
    ]
}

dataset = []

for i in range(1, 101):

    service, category = random.choice(services)

    region = random.choice(regions)

    template = random.choice(
        templates[service]
    )

    incident = template.format(
        region=region
    )

    dataset.append(
        {
            "id": i,
            "input": incident,
            "expected": {
                "service": service,
                "region": region,
                "category": category
            }
        }
    )

with open(
    "evaluations/gold_incident_dataset.json",
    "w"
) as f:

    json.dump(
        dataset,
        f,
        indent=4
    )

print("Generated 100 clean gold test cases.")