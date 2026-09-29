from ai.gap_engine.next_best_evidence import (
    recommend_next_best_evidence,
)


def test_case_design_is_recommended():
    result = recommend_next_best_evidence(
        [
            "CASE_DESIGN",
            "PRACTICAL_WORK",
        ]
    )

    assert result["status"] == "RECOMMENDED"
    assert result["target_dimension"] == "CASE_DESIGN"
    assert result["evidence_type"] == "CASE_STUDY"


def test_practical_work_is_recommended():
    result = recommend_next_best_evidence(
        ["PRACTICAL_WORK"]
    )

    assert result["evidence_type"] == "PRACTICAL"


def test_no_missing_dimensions_requires_no_action():
    result = recommend_next_best_evidence([])

    assert result["status"] == "NO_ACTION_REQUIRED"
    assert result["evidence_type"] is None


def test_unknown_dimension_is_not_assumed():
    result = recommend_next_best_evidence(
        ["UNKNOWN_DIMENSION"]
    )

    assert result["status"] == "UNKNOWN"