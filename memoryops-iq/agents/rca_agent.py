import os
import json


def calculate_pattern_frequency(
    root_cause
):

    incidents_path = (
        "data/incidents.json"
    )

    if not os.path.exists(
        incidents_path
    ):

        return {
            "occurrences": 0,
            "total": 0,
            "percentage": 0
        }

    with open(
        incidents_path,
        "r",
        encoding="utf-8"
    ) as f:

        incidents = json.load(f)

    total = len(
        incidents
    )

    occurrences = 0

    for incident in incidents:

        if (
            incident.get(
                "root_cause"
            )
            ==
            root_cause
        ):

            occurrences += 1

    percentage = 0

    if total > 0:

        percentage = round(
            (
                occurrences
                /
                total
            ) * 100,
            2
        )

    return {

        "occurrences":
            occurrences,

        "total":
            total,

        "percentage":
            percentage
    }


def recommend_rca(
    similar_incident,
    change_correlation,
    knowledge_fusion
):

    #
    # No Similar Incident
    #

    if not similar_incident:

        return {

            "historical_match_found":
                False,

            "incident_id":
                None,

            "primary_hypothesis":
                None,

            "likely_root_cause":
                None,

            "alternative_hypothesis":
                None,

            "historical_confidence":
                0,

            "change_found":
                False,

            "change_id":
                None,

            "change_type":
                None,

            "change_confidence":
                0,

            "rca_confidence":
                0,

            "pattern_frequency": {
                "occurrences": 0,
                "total": 0,
                "percentage": 0
            },

            "evidence": [],

            "reasoning":
                "No historical evidence available.",

            "rca":
                None
        }

    #
    # Local Incident Evidence
    #

    incident_data = (
        similar_incident.get(
            "incident",
            {}
        )
    )

    incident_id = (
        incident_data.get(
            "incident_id"
        )
    )

    primary_hypothesis = (
        incident_data.get(
            "root_cause"
        )
    )

    historical_confidence = round(
        min(
            similar_incident.get(
                "score",
                0
            ),
            1.0
        ) * 100,
        2
    )

    #
    # Change Evidence
    #

    change_found = (
        change_correlation.get(
            "change_found",
            False
        )
    )

    change_id = (
        change_correlation.get(
            "change_id"
        )
    )

    change_type = (
        change_correlation.get(
            "change_type"
        )
    )

    change_confidence = (
        change_correlation.get(
            "confidence",
            0
        )
    )

    #
    # Fusion Evidence
    #

    fusion_confidence = (
        knowledge_fusion.get(
            "confidence_score",
            0
        )
    )

    root_cause_candidates = (
        knowledge_fusion.get(
            "root_cause_candidates",
            []
        )
    )

    #
    # Alternative Hypothesis
    #

    alternative_hypothesis = None

    for candidate in root_cause_candidates:

        if (
            candidate.lower()
            !=
            primary_hypothesis.lower()
        ):

            alternative_hypothesis = candidate
            break

    if (
        alternative_hypothesis is None
        and
        change_type
):

        alternative_hypothesis = (
        change_type
    )

    #
    # Pattern Frequency
    #

    pattern_frequency = (
        calculate_pattern_frequency(
            primary_hypothesis
        )
    )

    #
    # RCA Confidence
    #

    final_confidence = round(
        (
            historical_confidence
            +
            fusion_confidence
        )
        / 2,
        2
    )

    #
    # RCA File
    #

    rca_text = None

    rca_path = (
        f"data/rcas/{incident_id}.txt"
    )

    if os.path.exists(
        rca_path
    ):

        with open(
            rca_path,
            "r",
            encoding="utf-8"
        ) as f:

            rca_text = f.read()

    #
    # Evidence
    #

    evidence = []

    evidence.append({

        "type":
            "historical_incident",

        "id":
            incident_id,

        "confidence":
            historical_confidence
    })

    if change_found:

        evidence.append({

            "type":
                "change_record",

            "id":
                change_id,

            "confidence":
                change_confidence
        })

    for incident in (
        knowledge_fusion.get(
            "validated_incidents",
            []
        )
    ):

        evidence.append({

            "type":
                "foundry_validation",

            "id":
                incident.get(
                    "incident_id"
                )
        })

    return {

        "historical_match_found":
            True,

        "incident_id":
            incident_id,
			
		"service":
            incident_data.get(
                "service"
            ),
		

        "primary_hypothesis":
            primary_hypothesis,

        "likely_root_cause":
            primary_hypothesis,

        "alternative_hypothesis":
            alternative_hypothesis,

        "historical_confidence":
            historical_confidence,

        "change_found":
            change_found,

        "change_id":
            change_id,

        "change_type":
            change_type,

        "change_confidence":
            change_confidence,

        "fusion_confidence":
            fusion_confidence,

        "final_confidence":
            final_confidence,

        "rca_confidence":
            final_confidence,

        "pattern_frequency":
            pattern_frequency,

        "supporting_evidence": [

            incident_id,
            change_id
        ],

        "evidence":
            evidence,

        "investigation_priority": [

            primary_hypothesis,
            alternative_hypothesis
        ],

        "reasoning":
            (
                f"Historical incident "
                f"{incident_id} identified "
                f"'{primary_hypothesis}' as "
                f"the most likely root cause. "
                f"Knowledge Fusion validated "
                f"supporting incident, change, "
                f"and runbook evidence."
            ),

        "rca":
            rca_text
    }


if __name__ == "__main__":

    print(
        json.dumps(
            {
                "message":
                    (
                        "RCA Agent is now a "
                        "consumer agent and "
                        "must be called from "
                        "the orchestrator."
                    )
            },
            indent=2
        )
    )