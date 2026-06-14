import os

os.makedirs("data/runbooks", exist_ok=True)

runbooks = {
    "VPN": [
        "Verify VPN Gateway health",
        "Check firewall ACL changes",
        "Validate route propagation",
        "Rollback recent network changes"
    ],
    "DNS": [
        "Check DNS server availability",
        "Validate DNS records",
        "Review recent configuration changes",
        "Flush DNS cache"
    ],
    "BGP": [
        "Verify BGP neighbors",
        "Check route advertisements",
        "Inspect route filters",
        "Rollback routing changes"
    ],
    "Storage": [
        "Verify storage account status",
        "Check replication health",
        "Review access policies",
        "Validate network access"
    ],
    "SQL": [
        "Check database connectivity",
        "Review active sessions",
        "Inspect deadlocks",
        "Validate maintenance activities"
    ],
    "Key Vault": [
        "Verify RBAC assignments",
        "Check secret expiration",
        "Validate network restrictions",
        "Review audit logs"
    ],
    "App Service": [
        "Check deployment status",
        "Review application logs",
        "Inspect scaling configuration",
        "Restart application instance"
    ]
}

for service, steps in runbooks.items():

    content = f"RUNBOOK\n\nService: {service}\n\nPurpose:\nStandard troubleshooting procedure for {service} incidents.\n\nProcedure:\n"

    for i, step in enumerate(steps, start=1):
        content += f"\n{i}. {step}"

    content += "\n\nEscalation:\nContact Platform Operations Team\n\nSuccess Criteria:\nService restored and monitoring alerts cleared."

    filename = f"data/runbooks/{service.lower()}_runbook.txt"

    with open(filename, "w") as f:
        f.write(content)

print("Generated runbooks successfully.")