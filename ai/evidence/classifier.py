"""
Evidence classification.

Classifies evidence into:
- evidence type
- evidence dimension

The initial implementation uses deterministic rules.
LLM classification can be added later without changing
the output contract.
"""


EVIDENCE_RULES = {
    "MCQ": "KNOWLEDGE",
    "QUIZ": "KNOWLEDGE",
    "MULTIPLE CHOICE": "KNOWLEDGE",

    "SCENARIO": "APPLIED_REASONING",
    "CASE": "CASE_DESIGN",
    "CASE STUDY": "CASE_DESIGN",
    "DESIGN": "CASE_DESIGN",

    "PRACTICAL": "PRACTICAL_WORK",
    "CODING": "PRACTICAL_WORK",
    "WORK SAMPLE": "PRACTICAL_WORK",
    "WORK EXPERIENCE": "PRACTICAL_WORK",
    "PORTFOLIO": "PRACTICAL_WORK",

    "CERTIFICATION": "KNOWLEDGE",
    "TRAINING COMPLETION": "KNOWLEDGE",
    "SELF REPORT": "KNOWLEDGE",
}


def classify_evidence(
    evidence_type: str,
    description: str = "",
) -> dict:
    """
    Classify an evidence item.

    Returns a stable structure that the capability engine
    can consume later.
    """

    normalized_type = evidence_type.strip().upper()

    dimension = EVIDENCE_RULES.get(
        normalized_type,
        "UNKNOWN",
    )

    confidence = 0.95 if dimension != "UNKNOWN" else 0.0

    return {
        "evidence_type": normalized_type,
        "evidence_dimension": dimension,
        "confidence": confidence,
        "description": description,
    }