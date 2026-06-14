import json

from agents.incident_understanding_agent import (
    classify_incident
)

from agents.similar_incident_agent import (
    find_best_match
)

from agents.change_correlation_agent import (
    find_correlated_change
)

from agents.knowledge_fusion_agent import (
    fuse_knowledge
)

from agents.rca_agent import (
    recommend_rca
)

from agents.remediation_planning_agent import (
    recommend_remediation
)

from agents.investigation_agent import (
    investigate_incident
)

from agents.impact_agent import (
    generate_impact
)

from agents.executive_summary_agent import (
    generate_executive_summary
)

from agents.overview_agent import (
    build_overview
)

from agents.foundry_iq_agent import (
    retrieve_foundry_context
)


def process_incident(
    incident_id,
    incident_text
):

    print(
        "\n=============================="
    )

    print(
        "MEMORYOPS IQ ORCHESTRATOR"
    )

    print(
        "==============================\n"
    )

    #
    # STEP 1
    # Incident Understanding
    #

    classification = (
        classify_incident(
            incident_text
        )
    )

    print(
        "\nCLASSIFICATION\n"
    )

    print(
        json.dumps(
            classification,
            indent=2
        )
    )

    #
    # STEP 2
    # Foundry IQ
    #

    print(
        "\nFOUNDRY IQ RETRIEVAL\n"
    )

    foundry_context = (
        retrieve_foundry_context(
            incident_text
        )
    )

    print(
        json.dumps(
            foundry_context,
            indent=2
        )
    )

    #
    # STEP 3
    # Similar Incident Agent
    #

    similar_incident = (
        find_best_match(
            incident_text,
			classification
        )
    )

    #
    # STEP 4
    # Change Correlation Agent
    #

    change_correlation = (
        find_correlated_change(
            incident_text,
			classification
        )
    )

    #
    # STEP 5
    # Knowledge Fusion Layer
    #

    fusion_result = (
        fuse_knowledge(
            similar_incident,
            change_correlation,
            foundry_context
        )
    )

    print(
        "\nKNOWLEDGE FUSION\n"
    )

    print(
        json.dumps(
            fusion_result,
            indent=2
        )
    )

    #
    # STEP 6
    # RCA Agent
    #

    rca_result = (
        recommend_rca(
            similar_incident,
            change_correlation,
            fusion_result
        )
    )

    #
    # STEP 7
    # Remediation Agent
    #

    remediation_result = (
        recommend_remediation(
            incident_text,
            classification,
            rca_result
        )
    )

    #
    # STEP 8
    # Investigation Agent
    #

    investigation_result = (
        investigate_incident(
            incident_text,
            remediation_result
        )
    )

    #
    # STEP 9
    # Impact Agent
    #

    impact_result = (
        generate_impact(
            incident_id,
            incident_text,
            classification,
            rca_result,
            remediation_result,
            investigation_result
        )
    )

    #
    # STEP 10
    # Executive Summary Agent
    #

    executive_summary = (
        generate_executive_summary(
            incident_id,
            incident_text,
            classification,
            rca_result,
            remediation_result,
            investigation_result,
            impact_result
        )
    )

    #
    # STEP 11
    # Overview Agent
    #

    overview = (
        build_overview(
            incident_id,
            incident_text,
            classification,
            rca_result,
            remediation_result,
            impact_result
        )
    )

    return {

        "overview":
            overview,

        "foundry_iq":
            foundry_context,

        "classification":
            classification,

        "similar_incident":
            similar_incident,

        "change_correlation":
            change_correlation,
		
		"similar_changes": {

            "primary_change":
                change_correlation,

            "related_changes": [
				
				change
				
                for change in foundry_context.get(
                    "related_change_records",
                    []
                )
				
				if (
					change.get(
						"change_id"
					)
					!=
					change_correlation.get(
						"change_id"
					)
				)
			]	
        },

        "knowledge_fusion":
            fusion_result,

        "root_cause_analysis":
            rca_result,

        "remediation":
            remediation_result,

        "investigation":
            investigation_result,

        "impact_analysis":
            impact_result,

        "executive_summary":
            executive_summary
    }


if __name__ == "__main__":

    incident_id = input(
        "Enter Incident ID: "
    )

    incident_text = input(
        "Enter Incident Description: "
    )

    result = (
        process_incident(
            incident_id,
            incident_text
        )
    )

    print(
        "\n=============================="
    )

    print(
        "FINAL MEMORYOPS IQ OUTPUT"
    )

    print(
        "==============================\n"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )