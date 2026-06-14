from openai import OpenAI
import json

API_KEY = "2KG3umFrYDIebzGUGsiXPByG0JtcvDZbN2dAshCyTVGbAJuKL8EmJQQJ99CFACHYHv6XJ3w3AAAAACOGJAAH"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://memoryops-iq-resource.services.ai.azure.com/openai/v1"
)


def classify_incident(incident_text):

    prompt = f"""
You are an enterprise IT incident classification engine.

Your task is to classify incidents using ONLY the following taxonomy.

VALID SERVICES:
- VPN
- DNS
- Firewall
- Routing
- Identity
- Certificate
- Key Vault
- Storage
- SQL
- App Service
- Unknown

IMPORTANT:

If the technology or service is not represented in the taxonomy:

Return:

"service":"Unknown"

Do NOT guess.
Do NOT map unsupported technologies.

VALID CATEGORIES:
- Network
- Security
- Cloud

REGION RULES:
- Extract region exactly if present.

Valid regions:
- APAC
- East US
- West Europe
- Global

If no region exists:
Return Global.

MAPPING RULES:

Azure SQL = SQL
Azure SQL Database = SQL
Blob Storage = Storage
Azure Storage = Storage
SSL = Certificate
HTTPS = Certificate
BGP = Routing
Authentication = Identity
MFA = Identity
Entra = Identity

Return ONLY JSON.

Example 1

Incident:
VPN outage affecting users in APAC

Output:
{{
    "service":"VPN",
    "region":"APAC",
    "category":"Network"
}}

Example 2

Incident:
Azure SQL database unavailable in East US

Output:
{{
    "service":"SQL",
    "region":"East US",
    "category":"Cloud"
}}

Example 3

Incident:
SSL certificate issue impacting applications in West Europe

Output:
{{
    "service":"Certificate",
    "region":"West Europe",
    "category":"Security"
}}

Example 4

Incident:
AKS cluster latency affecting workloads in East US

Output:
{{
    "service":"Unknown",
    "region":"East US",
    "category":"Cloud"
}}

Incident:
{incident_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    result = json.loads(content)

    service_map = {
        "entra": "Identity",
        "azure entra": "Identity",
        "microsoft entra": "Identity",
        "authentication": "Identity",
        "mfa": "Identity",
        "azure sql": "SQL",
        "azure sql database": "SQL",
        "azure storage": "Storage",
        "blob storage": "Storage",
        "bgp": "Routing",
        "network backbone": "Routing",
        "ssl": "Certificate",
        "https": "Certificate"
    }

    category_map = {
        "authentication": "Security",
        "identity": "Security",
        "access": "Security",
        "database": "Cloud",
        "availability": "Cloud",
        "deployment": "Cloud",
        "application": "Cloud",
        "access failures": "Cloud"
    }

    service = (
        str(
            result.get(
                "service",
                ""
            )
        )
        .strip()
    )

    category = (
        str(
            result.get(
                "category",
                ""
            )
        )
        .strip()
        .lower()
    )

    region = (
        str(
            result.get(
                "region",
                ""
            )
        )
        .strip()
    )

    #
    # Service Normalization
    #

    if service.lower() in service_map:

        result["service"] = (
            service_map[
                service.lower()
            ]
        )

    #
    # Category Normalization
    #

    if category in category_map:

        result["category"] = (
            category_map[
                category
            ]
        )

    #
    # Region Validation
    #

    if (
        region == ""
        or region.lower() == "unknown"
        or region.lower() == "none"
        or region.lower() == "null"
    ):

        result["region"] = "Global"

    #
    # Enterprise Service Validation
    #

    valid_services = [

        "VPN",
        "DNS",
        "Firewall",
        "Routing",
        "Identity",
        "Certificate",
        "Key Vault",
        "Storage",
        "SQL",
        "App Service",
        "Unknown"
    ]

    if (
        result.get("service")
        not in valid_services
    ):

        result["service"] = (
            "Unknown"
        )

    #
    # Enterprise Category Enforcement
    #

    service_category_map = {

        "VPN":
            "Network",

        "DNS":
            "Network",

        "Firewall":
            "Network",

        "Routing":
            "Network",

        "Identity":
            "Security",

        "Certificate":
            "Security",

        "Key Vault":
            "Security",

        "Storage":
            "Cloud",

        "SQL":
            "Cloud",

        "App Service":
            "Cloud",

        "Unknown":
            "Cloud"
    }

    service_name = (
        result.get(
            "service"
        )
    )

    if (
        service_name
        in
        service_category_map
    ):

        result["category"] = (
            service_category_map[
                service_name
            ]
        )

    return result


if __name__ == "__main__":

    incident = input(
        "Enter incident description: "
    )

    result = classify_incident(
        incident
    )

    print(
        "\nFINAL RESULT:"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )