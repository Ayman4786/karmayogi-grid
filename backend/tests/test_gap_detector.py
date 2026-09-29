from ai.gap_engine.gap_detector import detect_gap


def test_unknown_evidence_is_not_called_a_gap():
    result = detect_gap(
        required_level="L3",
        estimated_level=None,
        evidence_status="UNKNOWN",
    )

    assert result["status"] == "UNKNOWN"


def test_l2_against_l3_is_verified_gap():
    result = detect_gap(
        required_level="L3",
        estimated_level="L2",
        evidence_status="SUFFICIENT",
    )

    assert result["status"] == "VERIFIED_GAP"
    assert result["gap_level"] == 1


def test_l1_against_l3_is_two_level_gap():
    result = detect_gap(
        required_level="L3",
        estimated_level="L1",
        evidence_status="SUFFICIENT",
    )

    assert result["status"] == "VERIFIED_GAP"
    assert result["gap_level"] == 2


def test_required_level_is_met():
    result = detect_gap(
        required_level="L3",
        estimated_level="L3",
        evidence_status="SUFFICIENT",
    )

    assert result["status"] == "MEETS_REQUIREMENT"
    assert result["gap_level"] == 0


def test_higher_level_meets_requirement():
    result = detect_gap(
        required_level="L3",
        estimated_level="L4",
        evidence_status="SUFFICIENT",
    )

    assert result["status"] == "MEETS_REQUIREMENT"


def test_invalid_required_level_is_rejected():
    try:
        detect_gap(
            required_level="L5",
            estimated_level="L3",
            evidence_status="SUFFICIENT",
        )
        assert False
    except ValueError:
        assert True