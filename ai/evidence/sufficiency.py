"""
Evidence sufficiency engine.

Determines whether the available evidence covers the evidence
dimensions required for a competency level.

Important:
Insufficient evidence is UNKNOWN.
It must not automatically be treated as a capability weakness.
"""


def assess_evidence_sufficiency(
    required_dimensions: list[str],
    available_dimensions: list[str],
) -> dict:
    """
    Compare required evidence dimensions with available evidence.

    Returns:
        {
            "status": "SUFFICIENT" | "UNKNOWN",
            "required_dimensions": [...],
            "available_dimensions": [...],
            "missing_dimensions": [...]
        }
    """

    required = set(required_dimensions)
    available = set(available_dimensions)

    missing = required - available

    if missing:
        return {
            "status": "UNKNOWN",
            "required_dimensions": sorted(required),
            "available_dimensions": sorted(available),
            "missing_dimensions": sorted(missing),
        }

    return {
        "status": "SUFFICIENT",
        "required_dimensions": sorted(required),
        "available_dimensions": sorted(available),
        "missing_dimensions": [],
    }