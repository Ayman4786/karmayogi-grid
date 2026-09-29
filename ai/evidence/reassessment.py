"""
Reassessment engine.

Compares capability evidence before and after a new assessment.

The engine does not directly assign a capability level.
It determines whether the evidence state changed.
"""

from ai.evidence.capability import estimate_capability


def reassess_capability(
    previous_dimensions: dict[str, float],
    new_dimensions: dict[str, float],
) -> dict:
    """
    Compare previous evidence with newly collected evidence.

    New evidence replaces the score for a dimension when that
    dimension is present in new_dimensions.
    """

    combined_dimensions = dict(previous_dimensions)

    combined_dimensions.update(new_dimensions)

    previous_capability = estimate_capability(
        previous_dimensions
    )

    new_capability = estimate_capability(
        combined_dimensions
    )

    previous_level = previous_capability.get(
        "estimated_level"
    )

    new_level = new_capability.get(
        "estimated_level"
    )

    return {
        "previous_level": previous_level,
        "new_level": new_level,
        "changed": previous_level != new_level,
        "previous_dimensions": previous_dimensions,
        "new_dimensions": combined_dimensions,
    }