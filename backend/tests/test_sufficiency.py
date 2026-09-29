from ai.evidence.sufficiency import assess_evidence_sufficiency


def test_insufficient_evidence_is_unknown():
    result = assess_evidence_sufficiency(
        required_dimensions=[
            "KNOWLEDGE",
            "APPLIED_REASONING",
            "CASE_DESIGN",
            "PRACTICAL_WORK",
        ],
        available_dimensions=[
            "KNOWLEDGE",
            "APPLIED_REASONING",
        ],
    )

    assert result["status"] == "UNKNOWN"

    assert set(result["missing_dimensions"]) == {
        "CASE_DESIGN",
        "PRACTICAL_WORK",
    }


def test_sufficient_evidence():
    result = assess_evidence_sufficiency(
        required_dimensions=[
            "KNOWLEDGE",
            "APPLIED_REASONING",
        ],
        available_dimensions=[
            "KNOWLEDGE",
            "APPLIED_REASONING",
            "CASE_DESIGN",
        ],
    )

    assert result["status"] == "SUFFICIENT"
    assert result["missing_dimensions"] == []


def test_empty_evidence_is_unknown():
    result = assess_evidence_sufficiency(
        required_dimensions=["KNOWLEDGE"],
        available_dimensions=[],
    )

    assert result["status"] == "UNKNOWN"
    assert result["missing_dimensions"] == ["KNOWLEDGE"]