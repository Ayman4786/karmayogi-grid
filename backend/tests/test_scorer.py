import pytest

from ai.quiz.scorer import score_quiz


QUESTIONS = [
    {
        "id": "Q1",
        "correct_answer": "A",
        "evidence_dimension": "KNOWLEDGE",
    },
    {
        "id": "Q2",
        "correct_answer": "B",
        "evidence_dimension": "APPLIED_REASONING",
    },
    {
        "id": "Q3",
        "correct_answer": "C",
        "evidence_dimension": "CASE_DESIGN",
    },
]


def test_all_answers_correct():

    result = score_quiz(
        QUESTIONS,
        ["A", "B", "C"],
    )

    assert result["total_questions"] == 3
    assert result["correct_answers"] == 3
    assert result["score"] == 1.0


def test_partial_score():

    result = score_quiz(
        QUESTIONS,
        ["A", "X", "C"],
    )

    assert result["correct_answers"] == 2
    assert result["score"] == 0.6667


def test_all_answers_wrong():

    result = score_quiz(
        QUESTIONS,
        ["X", "X", "X"],
    )

    assert result["correct_answers"] == 0
    assert result["score"] == 0.0


def test_answer_count_must_match():

    with pytest.raises(ValueError):

        score_quiz(
            QUESTIONS,
            ["A"],
        )


def test_empty_quiz():

    result = score_quiz(
        [],
        [],
    )

    assert result["total_questions"] == 0
    assert result["correct_answers"] == 0
    assert result["score"] == 0.0
    assert result["results"] == []