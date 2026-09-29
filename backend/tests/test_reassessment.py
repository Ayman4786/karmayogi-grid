from ai.evidence.reassessment import (
    reassess_capability,
)


def test_reassessment_improves_capability():

    result = reassess_capability(
        previous_dimensions={
            "KNOWLEDGE": 0.80,
            "APPLIED_REASONING": 0.75,
        },
        new_dimensions={
            "CASE_DESIGN": 0.80,
            "PRACTICAL_WORK": 0.75,
        },
    )

    assert result["previous_level"] == "L2"
    assert result["new_level"] == "L3"
    assert result["changed"] is True


def test_reassessment_without_new_evidence():

    previous = {
        "KNOWLEDGE": 0.80,
        "APPLIED_REASONING": 0.75,
    }

    result = reassess_capability(
        previous_dimensions=previous,
        new_dimensions={},
    )

    assert result["previous_level"] == result["new_level"]
    assert result["changed"] is False


def test_reassessment_preserves_previous_dimensions():

    result = reassess_capability(
        previous_dimensions={
            "KNOWLEDGE": 0.80,
            "APPLIED_REASONING": 0.75,
        },
        new_dimensions={
            "CASE_DESIGN": 0.80,
        },
    )

    assert "KNOWLEDGE" in result["new_dimensions"]
    assert "APPLIED_REASONING" in result["new_dimensions"]
    assert "CASE_DESIGN" in result["new_dimensions"]