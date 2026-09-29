from fastapi import APIRouter, HTTPException

from ai.quiz.generator import generate_quiz_question
from ai.quiz.validator import validate_quiz_question
from ai.quiz.scorer import score_quiz

from ai.evidence.capability import estimate_capability
from ai.evidence.sufficiency import assess_evidence_sufficiency

from ai.gap_engine.gap_detector import detect_gap
from ai.gap_engine.next_best_evidence import (
    recommend_next_best_evidence,
)

from backend.app.schemas.assessment import (
    AssessmentGenerateRequest,
    AssessmentGenerateResponse,
    AssessmentSubmitRequest,
    AssessmentSubmitResponse,
)


router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"],
)


REQUIRED_DIMENSIONS = [
    "KNOWLEDGE",
    "APPLIED_REASONING",
    "CASE_DESIGN",
    "PRACTICAL_WORK",
]


@router.post(
    "/generate",
    response_model=AssessmentGenerateResponse,
)
def generate_assessment(
    request: AssessmentGenerateRequest,
):
    """
    Generate and validate one assessment question.
    """

    question = generate_quiz_question(
        competency_id=request.competency_id,
        level=request.level,
        context=request.context,
        source_ids=request.source_ids,
    )

    validation = validate_quiz_question(question)

    if not validation["valid"]:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Generated assessment failed validation.",
                "errors": validation["errors"],
            },
        )

    return {
        "question": question,
    }


@router.post(
    "/submit",
    response_model=AssessmentSubmitResponse,
)
def submit_assessment(
    request: AssessmentSubmitRequest,
):
    """
    Score the assessment and convert the result into evidence.

    The assessment itself does not determine capability.
    The capability engine interprets the resulting evidence.
    """

    question = request.question

    # --------------------------------------------------------
    # 1. Validate the question
    # --------------------------------------------------------

    validation = validate_quiz_question(question)

    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid assessment question.",
                "errors": validation["errors"],
            },
        )

    # --------------------------------------------------------
    # 2. Score the learner's answer
    # --------------------------------------------------------

    score = score_quiz(
        questions=[question],
        answers=[request.answer],
    )

    # --------------------------------------------------------
    # 3. Convert assessment result into evidence
    # --------------------------------------------------------

    assessment_score = score["score"]

    evidence_dimension = question.get(
        "evidence_dimension",
        "KNOWLEDGE",
    )

    evidence = {
        "dimension": evidence_dimension,
        "score": assessment_score,
        "assessment_type": "MCQ",
        "source_ids": question.get(
            "source_ids",
            [],
        ),
    }

    # --------------------------------------------------------
    # 4. Interpret evidence through capability engine
    # --------------------------------------------------------

    evidence_dimensions = {
        evidence_dimension: assessment_score,
    }

    capability = estimate_capability(
        evidence_dimensions,
    )

    # --------------------------------------------------------
    # 5. Check evidence sufficiency
    # --------------------------------------------------------

    evidence_status = assess_evidence_sufficiency(
        required_dimensions=REQUIRED_DIMENSIONS,
        available_dimensions=list(
            evidence_dimensions.keys()
        ),
    )

    # --------------------------------------------------------
    # 6. Detect gap / uncertainty
    # --------------------------------------------------------

    gap = detect_gap(
        required_level=question["level"],
        estimated_level=capability.get(
            "estimated_level"
        ),
        evidence_status=evidence_status["status"],
    )

    # --------------------------------------------------------
    # 7. Recommend next-best evidence
    # --------------------------------------------------------

    next_best_evidence = (
        recommend_next_best_evidence(
            evidence_status["missing_dimensions"]
        )
    )

    return {
        "score": score,
        "evidence": evidence,
        "capability": capability,
        "evidence_status": evidence_status,
        "gap": gap,
        "next_best_evidence": next_best_evidence,
    }