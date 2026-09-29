"""
Quiz generation.

Provides a structured quiz-generation interface.

The current implementation creates a deterministic question from
retrieved source context. An LLM can later replace the generation
logic while preserving this output contract.
"""


def generate_quiz_question(
    competency_id: str,
    level: str,
    context: str,
    source_ids: list[str],
) -> dict:
    """
    Generate one structured assessment question.
    """

    if not context.strip():
        raise ValueError("Context is required for quiz generation.")

    if not source_ids:
        raise ValueError("At least one source is required.")

    question = (
        f"Which statement is most appropriate for "
        f"{competency_id} at {level}?"
    )

    options = [
        "Select and justify an appropriate approach.",
        "Memorize terminology without applying it.",
        "Ignore the characteristics of the problem.",
        "Use the same approach for every situation.",
    ]

    return {
        "question": question,
        "options": options,
        "correct_answer": options[0],
        "explanation": (
            "The correct answer requires selecting an appropriate "
            "approach and justifying the decision."
        ),
        "competency_id": competency_id,
        "level": level,
        "source_ids": source_ids,
    }