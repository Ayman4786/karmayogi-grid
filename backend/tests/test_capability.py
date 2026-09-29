from ai.evidence.capability import estimate_capability


def test_l1_capability():
    result = estimate_capability(
        {
            "KNOWLEDGE": 0.80,
        }
    )

    assert result["status"] == "ESTIMATED"
    assert result["estimated_level"] == "L1"


def test_l2_capability():
    result = estimate_capability(
        {
            "KNOWLEDGE": 0.80,
            "APPLIED_REASONING": 0.75,
        }
    )

    assert result["status"] == "ESTIMATED"
    assert result["estimated_level"] == "L2"


def test_l3_requires_all_four_dimensions():
    result = estimate_capability(
        {
            "KNOWLEDGE": 0.90,
            "APPLIED_REASONING": 0.85,
            "CASE_DESIGN": 0.80,
            "PRACTICAL_WORK": 0.75,
        }
    )

    assert result["status"] == "ESTIMATED"
    assert result["estimated_level"] == "L3"


def test_l4_requires_higher_score():
    result = estimate_capability(
        {
            "KNOWLEDGE": 0.90,
            "APPLIED_REASONING": 0.90,
            "CASE_DESIGN": 0.85,
            "PRACTICAL_WORK": 0.85,
        }
    )

    assert result["status"] == "ESTIMATED"
    assert result["estimated_level"] == "L4"


def test_missing_dimensions_do_not_create_l3():
    result = estimate_capability(
        {
            "KNOWLEDGE": 0.90,
            "APPLIED_REASONING": 0.90,
        }
    )

    assert result["estimated_level"] == "L2"


def test_empty_evidence_is_unknown():
    result = estimate_capability({})

    assert result["status"] == "UNKNOWN"
    assert result["estimated_level"] is None


def test_invalid_score_is_rejected():
    try:
        estimate_capability({"KNOWLEDGE": 1.5})
        assert False
    except ValueError:
        assert True