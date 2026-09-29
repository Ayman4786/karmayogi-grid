"""
Quiz validation.

Validates generated assessment questions before they
are accepted by the assessment pipeline.
"""


VALID_LEVELS = {"L1", "L2", "L3", "L4"}


def validate_quiz_question(question: dict) -> dict:
    """
    Validate a generated quiz question.

    Returns:
        {
            "valid": bool,
            "errors": [...]
        }
    """

    errors = []

    # Question text
    if not question.get("question", "").strip():
        errors.append("QUESTION_MISSING")

    # Options
    options = question.get("options", [])

    if len(options) != 4:
        errors.append("INVALID_OPTION_COUNT")

    # Correct answer
    correct_answer = question.get("correct_answer")

    if correct_answer not in options:
        errors.append("INVALID_CORRECT_ANSWER")

    # Competency
    if not question.get("competency_id"):
        errors.append("COMPETENCY_MISSING")

    # Level
    if question.get("level") not in VALID_LEVELS:
        errors.append("INVALID_LEVEL")

    # Source grounding
    if not question.get("source_ids"):
        errors.append("SOURCE_MISSING")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }