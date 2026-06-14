import json


def normalize(
    value
):

    if value is None:
        return ""

    return (
        str(value)
        .lower()
        .strip()
    )


def fuse_knowledge(
    similar_incident,
    change_correlation,
    foundry_context
):

    validated_incidents = []
    validated_changes = []
    validated_runbooks = []

    confidence = 50

    #
    # Local Evidence
    #

    local_incident = (
        similar_incident
        .get(
            "incident",
            {}
        )
        .get(
            "incident_id"
        )
    )

    local_root_cause = (
        similar_incident
        .get(
            "incident",
            {}
        )
        .get(
            "root_cause"
        )
    )

    local_change = (
        change_correlation
        .get(
            "change_id"
        )
    )

    local_change_type = (
        change_correlation
        .get(
            "change_type"
        )
    )

    #
    # Foundry Incidents
    #

    foundry_incidents = (
        foundry_context
        .get(
            "similar_incidents",
            []
        )
    )

    for incident in foundry_incidents:

        incident_id = (
            incident.get(
                "incident_id"
            )
        )

        incident_root_cause = (
            incident.get(
                "root_cause"
            )
        )

        #
        # Exact Incident Match
        #

        if (
            incident_id
            ==
            local_incident
        ):

            validated_incidents.append(
                incident
            )

            confidence += 15

        #
        # Root Cause Match
        #

        elif (
            normalize(
                incident_root_cause
            )
            ==
            normalize(
                local_root_cause
            )
        ):

            validated_incidents.append(
                incident
            )

            confidence += 10

    #
    # Foundry Changes
    #

    foundry_changes = (
        foundry_context
        .get(
            "related_change_records",
            []
        )
    )

    for change in foundry_changes:

        change_id = (
            change.get(
                "change_id"
            )
        )

        description = normalize(
            change.get(
                "description",
                ""
            )
        )

        #
        # Exact Change Match
        #

        if (
            change_id
            ==
            local_change
        ):

            validated_changes.append(
                change
            )

            confidence += 15

        #
        # Change Type Match
        #

        elif (
            normalize(
                local_change_type
            )
            in
            description
        ):

            validated_changes.append(
                change
            )

            confidence += 10

    #
    # Runbooks
    #

    validated_runbooks = (
        foundry_context.get(
            "runbooks",
            []
        )
    )

    if len(
        validated_runbooks
    ) > 0:

        confidence += 10

    #
    # Root Cause Candidates
    #

    root_cause_candidates = (
        foundry_context.get(
            "likely_root_causes",
            []
        )
    )

    if len(
        root_cause_candidates
    ) > 0:

        confidence += 5

    #
    # Evidence
    #

    evidence = (
        foundry_context.get(
            "evidence",
            []
        )
    )

    if len(
        evidence
    ) > 0:

        confidence += 5

    confidence = min(
        confidence,
        100
    )

    return {

        "validated_incidents":
            validated_incidents,

        "validated_changes":
            validated_changes,

        "validated_runbooks":
            validated_runbooks,

        "root_cause_candidates":
            root_cause_candidates,

        "confidence_score":
            confidence,

        "evidence":
            evidence,

        "evidence_summary": {

            "local_incident":
                local_incident,

            "local_root_cause":
                local_root_cause,

            "local_change":
                local_change,

            "local_change_type":
                local_change_type,

            "validated_incident_count":
                len(
                    validated_incidents
                ),

            "validated_change_count":
                len(
                    validated_changes
                ),

            "validated_runbook_count":
                len(
                    validated_runbooks
                )
        }
    }


if __name__ == "__main__":

    similar_incident = {
        "incident": {
            "incident_id": "INC-1001",
            "root_cause": "DNS server outage"
        }
    }

    change_correlation = {
        "change_id": "CHG-1023",
        "change_type": "DNS Zone Update"
    }

    foundry_context = {
        "similar_incidents": [
            {
                "incident_id": "INC-1011",
                "root_cause": "DNS Server Outage"
            }
        ],
        "related_change_records": [
            {
                "change_id": "CHG-1023",
                "description": "DNS Zone Update"
            }
        ],
        "runbooks": [
            {
                "runbook_id": "dns_runbook.txt"
            }
        ],
        "likely_root_causes": [
            "DNS Server Outage"
        ]
    }

    result = fuse_knowledge(
        similar_incident,
        change_correlation,
        foundry_context
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )