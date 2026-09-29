"""
Next-Best Evidence engine.

Recommends the smallest useful assessment/evidence type that can
reduce uncertainty about a competency level.

This is deterministic decision logic. AI can later improve the
wording or generate the actual assessment.
"""


EVIDENCE_RECOMMENDATIONS = {
    "KNOWLEDGE": {
        "evidence_type": "MCQ",
        "action": "Complete a knowledge assessment.",
    },
    "APPLIED_REASONING": {
        "evidence_type": "SCENARIO",
        "action": "Complete an applied reasoning scenario.",
    },
    "CASE_DESIGN": {
        "evidence_type": "CASE_STUDY",
        "action": "Complete a competency-specific design case.",
    },
    "PRACTICAL_WORK": {
        "evidence_type": "PRACTICAL",
        "action": "Complete a practical work-based assessment.",
    },
}


def recommend_next_best_evidence(
    missing_dimensions: list[str],
) -> dict:
    """
    Recommend the next evidence needed to reduce uncertainty.

    The first missing dimension is selected as the next-best
    evidence target.
    """

    if not missing_dimensions:
        return {
            "status": "NO_ACTION_REQUIRED",
            "target_dimension": None,
            "evidence_type": None,
            "action": None,
        }

    target = missing_dimensions[0]

    recommendation = EVIDENCE_RECOMMENDATIONS.get(target)

    if recommendation is None:
        return {
            "status": "UNKNOWN",
            "target_dimension": target,
            "evidence_type": None,
            "action": "Collect additional evidence.",
        }

    return {
        "status": "RECOMMENDED",
        "target_dimension": target,
        "evidence_type": recommendation["evidence_type"],
        "action": recommendation["action"],
    }