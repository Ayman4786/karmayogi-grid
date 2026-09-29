"""
End-to-end capability intelligence pipeline test.

Flow:

Evidence
→ Classification
→ Sufficiency
→ Capability
→ Gap
→ Next-Best Evidence
"""

from ai.evidence.classifier import classify_evidence
from ai.evidence.sufficiency import assess_evidence_sufficiency
from ai.evidence.capability import estimate_capability
from ai.gap_engine.gap_detector import detect_gap
from ai.gap_engine.next_best_evidence import (
    recommend_next_best_evidence,
)


def test_sampling_l3_capability_pipeline():

    # --------------------------------------------------------
    # 1. Existing learner evidence
    # --------------------------------------------------------

    evidence_items = [
        classify_evidence("MCQ"),
        classify_evidence("Scenario"),
    ]

    available_dimensions = [
        item["evidence_dimension"]
        for item in evidence_items
    ]

    # --------------------------------------------------------
    # 2. Check evidence sufficiency for L3
    # --------------------------------------------------------

    required_dimensions = [
        "KNOWLEDGE",
        "APPLIED_REASONING",
        "CASE_DESIGN",
        "PRACTICAL_WORK",
    ]

    sufficiency = assess_evidence_sufficiency(
        required_dimensions=required_dimensions,
        available_dimensions=available_dimensions,
    )

    assert sufficiency["status"] == "UNKNOWN"

    assert set(sufficiency["missing_dimensions"]) == {
        "CASE_DESIGN",
        "PRACTICAL_WORK",
    }

    # --------------------------------------------------------
    # 3. Estimate current capability from available evidence
    # --------------------------------------------------------

    capability = estimate_capability(
        {
            "KNOWLEDGE": 0.85,
            "APPLIED_REASONING": 0.80,
        }
    )

    assert capability["estimated_level"] == "L2"

    # --------------------------------------------------------
    # 4. Compare against role requirement
    # --------------------------------------------------------

    gap = detect_gap(
        required_level="L3",
        estimated_level=capability["estimated_level"],
        evidence_status=sufficiency["status"],
    )

    # Because evidence is insufficient, this remains UNKNOWN.
    assert gap["status"] == "UNKNOWN"

    # --------------------------------------------------------
    # 5. Recommend next-best evidence
    # --------------------------------------------------------

    recommendation = recommend_next_best_evidence(
        sufficiency["missing_dimensions"]
    )

    assert recommendation["status"] == "RECOMMENDED"

    assert recommendation["target_dimension"] == "CASE_DESIGN"

    assert recommendation["evidence_type"] == "CASE_STUDY"