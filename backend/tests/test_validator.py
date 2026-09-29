from ai.quiz.validator import validate_quiz_question


VALID_QUESTION = {
    "question": "Which sampling approach is appropriate?",
    "options": [
        "Stratified sampling",
        "Random guessing",
        "Ignoring the population",
        "Using no sampling method",
    ],
    "correct_answer": "Stratified sampling",
    "competency_id": "STAT.SAMPLING",
    "level": "L3",
    "source_ids": ["SRC-001"],
}


def test_valid_question():

    result = validate_quiz_question(
        VALID_QUESTION
    )

    assert result["valid"] is True
    assert result["errors"] == []


def test_missing_question():

    question = {
        **VALID_QUESTION,
        "question": "",
    }

    result = validate_quiz_question(question)

    assert result["valid"] is False
    assert "QUESTION_MISSING" in result["errors"]


def test_invalid_option_count():

    question = {
        **VALID_QUESTION,
        "options": ["A", "B"],
    }

    result = validate_quiz_question(question)

    assert result["valid"] is False
    assert "INVALID_OPTION_COUNT" in result["errors"]


def test_invalid_correct_answer():

    question = {
        **VALID_QUESTION,
        "correct_answer": "Not an option",
    }

    result = validate_quiz_question(question)

    assert result["valid"] is False
    assert "INVALID_CORRECT_ANSWER" in result["errors"]


def test_invalid_level():

    question = {
        **VALID_QUESTION,
        "level": "L5",
    }

    result = validate_quiz_question(question)

    assert result["valid"] is False
    assert "INVALID_LEVEL" in result["errors"]


def test_missing_source():

    question = {
        **VALID_QUESTION,
        "source_ids": [],
    }

    result = validate_quiz_question(question)

    assert result["valid"] is False
    assert "SOURCE_MISSING" in result["errors"]