"""
Capability level estimation.

Prototype evidence-based capability rubric.

Important:
- L1-L4 are prototype project levels and require SME validation.
- Capability estimates must retain the evidence behind them.
- Insufficient evidence should remain UNKNOWN.
"""

LEVEL_REQUIREMENTS = {
    "L1": {
        "dimensions": {"KNOWLEDGE"},
        "minimum_score": 0.60,
    },
    "L2": {
        "dimensions": {
            "KNOWLEDGE",
            "APPLIED_REASONING",
        },
        "minimum_score": 0.60,
    },
    "L3": {
        "dimensions": {
            "KNOWLEDGE",
            "APPLIED_REASONING",
            "CASE_DESIGN",
            "PRACTICAL_WORK",
        },
        "minimum_score": 0.60,
    },
    "L4": {
        "dimensions": {
            "KNOWLEDGE",
            "APPLIED_REASONING",
            "CASE_DESIGN",
            "PRACTICAL_WORK",
        },
        "minimum_score": 0.85,
    },
}


def estimate_capability(
    dimension_scores: dict[str, float],
) -> dict:
    """
    Estimate the highest supported prototype capability level.

    dimension_scores example:

    {
        "KNOWLEDGE": 0.90,
        "APPLIED_REASONING": 0.80,
        "CASE_DESIGN": 0.75,
        "PRACTICAL_WORK": 0.70,
    }
    """

    if not dimension_scores:
        return {
            "status": "UNKNOWN",
            "estimated_level": None,
            "score": 0.0,
            "dimension_scores": {},
            "missing_dimensions": [],
            "confidence": 0.0,
        }

    # Validate scores.
    for dimension, score in dimension_scores.items():
        if not 0.0 <= score <= 1.0:
            raise ValueError(
                f"Score for {dimension} must be between 0 and 1."
            )

    # Check highest level first.
    for level in ("L4", "L3", "L2", "L1"):

        requirements = LEVEL_REQUIREMENTS[level]
        required_dimensions = requirements["dimensions"]

        missing_dimensions = (
            required_dimensions
            - set(dimension_scores.keys())
        )

        if missing_dimensions:
            continue

        score = sum(
            dimension_scores[dimension]
            for dimension in required_dimensions
        ) / len(required_dimensions)

        if score >= requirements["minimum_score"]:
            return {
                "status": "ESTIMATED",
                "estimated_level": level,
                "score": round(score, 4),
                "dimension_scores": dimension_scores,
                "missing_dimensions": [],
                "confidence": round(score, 4),
            }

    return {
        "status": "UNKNOWN",
        "estimated_level": None,
        "score": 0.0,
        "dimension_scores": dimension_scores,
        "missing_dimensions": [],
        "confidence": 0.0,
    }