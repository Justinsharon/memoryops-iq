def classify_incident(text):

    text = text.lower()

    service = "Unknown"
    region = "Global"
    category = "Unknown"

    #
    # Service Detection
    #

    if "vpn" in text:

        service = "VPN"
        category = "Network"

    elif "dns" in text:

        service = "DNS"
        category = "Network"

    elif "bgp" in text:

        service = "BGP"
        category = "Network"

    elif "storage" in text:

        service = "Storage"
        category = "Cloud"

    elif "sql" in text or "database" in text:

        service = "SQL"
        category = "Database"

    elif "key vault" in text:

        service = "Key Vault"
        category = "Security"

    elif "app service" in text:

        service = "App Service"
        category = "Cloud"

    elif "entra" in text or "authenticate" in text:

        service = "Identity"
        category = "Security"

    #
    # Region Detection
    #

    if "apac" in text:

        region = "APAC"

    elif "emea" in text:

        region = "EMEA"

    elif "europe" in text:

        region = "Europe"

    elif "east us" in text:

        region = "East US"

    elif "west us" in text:

        region = "West US"

    return {
        "service": service,
        "region": region,
        "category": category
    }