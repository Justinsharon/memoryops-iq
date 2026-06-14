import json


def build_overview(
    incident_id,
    incident_text,
    classification,
    rca_result,
    remediation_result,
    impact_result
):

    return {

        "incident_summary": {

            "incident_id":
                incident_id,

            "incident_description":
                incident_text,

            "service":
                classification.get(
                    "service"
                ),

            "region":
                classification.get(
                    "region"
                ),

            "category":
                classification.get(
                    "category"
                ),

            "confidence_score":
                rca_result.get(
                    "rca_confidence",
                    0
                ),

            "historical_match_found":
                rca_result.get(
                    "historical_match_found",
                    False
                )
        },

        "likely_root_cause": {

            "root_cause":
                rca_result.get(
                    "likely_root_cause"
                ),

            "alternative_hypothesis":
                rca_result.get(
                    "alternative_hypothesis"
                ),

            "pattern_frequency":
                rca_result.get(
                    "pattern_frequency",
                    {}
                ),

            "rca_confidence":
                rca_result.get(
                    "rca_confidence",
                    0
                ),

            "reasoning":
                rca_result.get(
                    "reasoning",
                    ""
                )
        },

        "recommended_actions": {

            "execution_status":
                remediation_result.get(
                    "execution_status"
                ),

            "action_count":
                len(
                    remediation_result.get(
                        "recommended_actions",
                        []
                    )
                ),

            "top_actions":
                remediation_result.get(
                    "recommended_actions",
                    []
                )[:4],

            "runbook_available":
                (
                    remediation_result.get(
                        "source"
                    )
                    ==
                    "runbook_enhanced"
                )
        },

        "impact_analysis": {

            "users_affected":
                impact_result.get(
                    "users_affected"
                ),

            "business_impact":
                impact_result.get(
                    "business_impact"
                ),

            "mttr_improvement":
                impact_result.get(
                    "mttr_improvement"
                ),

            "potential_downtime":
                impact_result.get(
                    "potential_downtime"
                )
        }
    }


if __name__ == "__main__":

    print(
        json.dumps(
            {
                "message":
                    (
                        "Overview Agent is a "
                        "consumer agent and "
                        "must be called from "
                        "the orchestrator."
                    )
            },
            indent=2
        )
    )