from ai.evidence.classifier import classify_evidence


def test_mcq_is_knowledge():
    result = classify_evidence("MCQ")

    assert result["evidence_dimension"] == "KNOWLEDGE"


def test_scenario_is_applied_reasoning():
    result = classify_evidence("Scenario")

    assert result["evidence_dimension"] == "APPLIED_REASONING"


def test_case_study_is_case_design():
    result = classify_evidence("Case Study")

    assert result["evidence_dimension"] == "CASE_DESIGN"


def test_practical_is_practical_work():
    result = classify_evidence("Practical")

    assert result["evidence_dimension"] == "PRACTICAL_WORK"


def test_unknown_evidence_is_not_assumed():
    result = classify_evidence("Something Unknown")

    assert result["evidence_dimension"] == "UNKNOWN"
    assert result["confidence"] == 0.0