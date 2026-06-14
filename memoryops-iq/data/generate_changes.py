import os
import json
import random
from datetime import datetime, timedelta

os.makedirs("data/changes", exist_ok=True)

with open("data/incidents.json", "r") as f:
    incidents = json.load(f)

services = [
    "VPN",
    "DNS",
    "SQL",
    "Storage",
    "Key Vault",
    "App Service",
    "BGP"
]

regions = [
    "APAC",
    "East US",
    "West Europe",
    "Global"
]

change_catalog = {
    "VPN": [
        "Firewall ACL Change",
        "VPN Gateway Upgrade",
        "Certificate Renewal",
        "Route Propagation Update"
    ],
    "DNS": [
        "DNS Zone Update",
        "DNS Forwarder Change",
        "DNS Server Patch",
        "DNS Configuration Update"
    ],
    "SQL": [
        "Database Maintenance",
        "Index Rebuild",
        "Connection Pool Configuration",
        "SQL Patch Deployment"
    ],
    "Storage": [
        "Storage Account Configuration",
        "Replication Configuration Update",
        "Access Policy Modification",
        "Network Access Update"
    ],
    "Key Vault": [
        "RBAC Change",
        "Secret Rotation",
        "Network Restriction Update",
        "Access Policy Change"
    ],
    "App Service": [
        "Application Deployment",
        "Scaling Configuration Change",
        "Runtime Upgrade",
        "CI/CD Pipeline Update"
    ],
    "BGP": [
        "Route Policy Update",
        "Neighbor Configuration Change",
        "Route Filter Update",
        "Routing Configuration Change"
    ]
}

risk_levels = [
    "Low",
    "Medium",
    "High"
]

approvals = [
    "Approved",
    "Emergency Approved",
    "Standard Approved"
]

engineers = [
    "Network Operations Team",
    "Cloud Operations Team",
    "Platform Engineering Team",
    "Infrastructure Team"
]

validation_results = [
    "Passed",
    "Passed",
    "Passed",
    "Passed",
    "Passed with Warnings",
    "Failed"
]

statuses = [
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Successful",
    "Partially Successful",
    "Partially Successful",
    "Rolled Back",
    "Failed",
    "Unsuccessful"
]

change_counter = 1001

for service in services:

    for _ in range(14):

        region = random.choice(regions)

        change_type = random.choice(
            change_catalog[service]
        )

        risk_level = random.choice(
            risk_levels
        )

        approval = random.choice(
            approvals
        )

        engineer = random.choice(
            engineers
        )

        validation = random.choice(
            validation_results
        )

        status = random.choice(
            statuses
        )

        age_bucket = random.randint(1, 100)

        if age_bucket <= 70:

            age_hours = random.randint(
                1,
                72
            )

        elif age_bucket <= 90:

            age_hours = random.randint(
                73,
                336
            )

        else:

            age_hours = random.randint(
                337,
                720
            )

        start_time = (
            datetime.now()
            - timedelta(
                hours=age_hours
            )
        )

        end_time = (
            start_time
            + timedelta(
                minutes=random.randint(
                    10,
                    60
                )
            )
        )

        change_text = f"""
CHANGE RECORD

Change ID: CHG-{change_counter}

Service:
{service}

Region:
{region}

Change Type:
{change_type}

Risk Level:
{risk_level}

Change Start:
{start_time.strftime("%Y-%m-%d %H:%M:%S")}

Change End:
{end_time.strftime("%Y-%m-%d %H:%M:%S")}

Implemented By:
{engineer}

Approval Status:
{approval}

Implementation Summary:
A planned change was implemented affecting {service}.

Validation Result:
{validation}

Rollback Plan:
Rollback to previous known-good configuration.

Status:
{status}
"""

        filename = (
            f"data/changes/CHG-{change_counter}.txt"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(change_text)

        change_counter += 1

print("Generated 98 enterprise-grade change records.")