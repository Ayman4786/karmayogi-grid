"""
Learning resource matcher.

Ranks learning resources against a competency requirement.

The initial implementation uses deterministic matching so that
the recommendation behavior is explainable and testable.
Vector/BM25 retrieval can be added later.
"""


def match_learning_resources(
    competency_id: str,
    required_level: str,
    resources: list[dict],
    evidence_dimension: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    """
    Rank resources for a competency requirement.
    """

    scored_resources = []

    for resource in resources:

        score = 0.0
        reasons = []

        # Competency match
        if competency_id in resource.get("competency_ids", []):
            score += 0.50
            reasons.append("competency_match")

        # Level match
        if required_level in resource.get("levels", []):
            score += 0.30
            reasons.append("level_match")

        # Evidence dimension match
        if (
            evidence_dimension
            and evidence_dimension
            in resource.get("evidence_dimensions", [])
        ):
            score += 0.20
            reasons.append("evidence_dimension_match")

        if score > 0:
            scored_resources.append(
                {
                    **resource,
                    "score": round(score, 4),
                    "match_reasons": reasons,
                }
            )

    scored_resources.sort(
        key=lambda resource: resource["score"],
        reverse=True,
    )

    return scored_resources[:top_k]