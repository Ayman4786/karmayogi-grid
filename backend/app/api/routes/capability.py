from fastapi import APIRouter

from ai.evidence.capability import estimate_capability
from ai.evidence.sufficiency import assess_evidence_sufficiency
from ai.gap_engine.gap_detector import detect_gap
from ai.gap_engine.next_best_evidence import (
    recommend_next_best_evidence,
)

from backend.app.schemas.capability_evaluation import (
    CapabilityEvaluationRequest,
    CapabilityEvaluationResponse,
)


router = APIRouter(
    prefix="/capability",
    tags=["Capability"],
)


REQUIRED_DIMENSIONS = [
    "KNOWLEDGE",
    "APPLIED_REASONING",
    "CASE_DESIGN",
    "PRACTICAL_WORK",
]


@router.post(
    "/evaluate",
    response_model=CapabilityEvaluationResponse,
)
def evaluate_capability(
    request: CapabilityEvaluationRequest,
):
    # --------------------------------------------------------
    # 1. Estimate capability
    # --------------------------------------------------------

    capability = estimate_capability(
        request.evidence_dimensions
    )

    # --------------------------------------------------------
    # 2. Determine evidence sufficiency
    # --------------------------------------------------------

    available_dimensions = list(
        request.evidence_dimensions.keys()
    )

    evidence_status = assess_evidence_sufficiency(
        required_dimensions=REQUIRED_DIMENSIONS,
        available_dimensions=available_dimensions,
    )

    # --------------------------------------------------------
    # 3. Detect gap
    # --------------------------------------------------------

    gap = detect_gap(
        required_level=request.required_level,
        estimated_level=capability.get(
            "estimated_level"
        ),
        evidence_status=evidence_status["status"],
    )

    # --------------------------------------------------------
    # 4. Recommend next-best evidence
    # --------------------------------------------------------

    next_best_evidence = (
        recommend_next_best_evidence(
            evidence_status["missing_dimensions"]
        )
    )

    return {
        "capability": capability,
        "evidence_status": evidence_status,
        "gap": gap,
        "next_best_evidence": next_best_evidence,
    }