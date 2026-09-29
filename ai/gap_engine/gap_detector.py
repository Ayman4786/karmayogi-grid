"""
Skill gap detection.

Compares a role's required competency level with the learner's
estimated capability level.

Important:
- UNKNOWN capability is not automatically a gap.
- VERIFIED_GAP requires demonstrated capability below the requirement.
- L1-L4 ordering is a prototype project scale requiring SME validation.
"""

LEVEL_ORDER = {
    "L1": 1,
    "L2": 2,
    "L3": 3,
    "L4": 4,
}


def detect_gap(
    required_level: str,
    estimated_level: str | None,
    evidence_status: str,
) -> dict:
    """
    Determine the learner's requirement status.

    Returns:
        UNKNOWN
        VERIFIED_GAP
        MEETS_REQUIREMENT
    """

    if required_level not in LEVEL_ORDER:
        raise ValueError(
            f"Invalid required level: {required_level}"
        )

    if estimated_level is not None and estimated_level not in LEVEL_ORDER:
        raise ValueError(
            f"Invalid estimated level: {estimated_level}"
        )

    if evidence_status != "SUFFICIENT":
        return {
            "status": "UNKNOWN",
            "required_level": required_level,
            "estimated_level": estimated_level,
            "gap_level": None,
        }

    if estimated_level is None:
        return {
            "status": "UNKNOWN",
            "required_level": required_level,
            "estimated_level": None,
            "gap_level": None,
        }

    required_value = LEVEL_ORDER[required_level]
    estimated_value = LEVEL_ORDER[estimated_level]

    if estimated_value < required_value:
        return {
            "status": "VERIFIED_GAP",
            "required_level": required_level,
            "estimated_level": estimated_level,
            "gap_level": required_value - estimated_value,
        }

    return {
        "status": "MEETS_REQUIREMENT",
        "required_level": required_level,
        "estimated_level": estimated_level,
        "gap_level": 0,
    }