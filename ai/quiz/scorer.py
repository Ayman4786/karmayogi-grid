"""
Deterministic assessment scorer.

The scorer evaluates answers.
It does NOT decide the learner's final capability level.
Capability estimation remains the responsibility of
ai.evidence.capability.
"""


def score_quiz(
    questions: list[dict],
    answers: list[str],
) -> dict:
    """
    Score a completed quiz.

    Each question must contain:
        correct_answer
        evidence_dimension (optional)

    Returns total score and per-question results.
    """

    if len(questions) != len(answers):
        raise ValueError(
            "Number of answers must match number of questions."
        )

    if not questions:
        return {
            "total_questions": 0,
            "correct_answers": 0,
            "score": 0.0,
            "results": [],
        }

    results = []
    correct_count = 0

    for question, answer in zip(
        questions,
        answers,
    ):

        is_correct = (
            answer == question["correct_answer"]
        )

        if is_correct:
            correct_count += 1

        results.append(
            {
                "question_id": question.get("id"),
                "correct": is_correct,
                "evidence_dimension": question.get(
                    "evidence_dimension"
                ),
            }
        )

    score = correct_count / len(questions)

    return {
        "total_questions": len(questions),
        "correct_answers": correct_count,
        "score": round(score, 4),
        "results": results,
    }