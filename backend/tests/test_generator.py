import pytest

from ai.quiz.generator import generate_quiz_question


def test_quiz_generation():

    result = generate_quiz_question(
        competency_id="STAT.SAMPLING",
        level="L3",
        context=(
            "Sampling design requires selecting and justifying "
            "an appropriate sampling strategy."
        ),
        source_ids=["SRC-001"],
    )

    assert result["competency_id"] == "STAT.SAMPLING"
    assert result["level"] == "L3"

    assert len(result["options"]) == 4

    assert result["correct_answer"] in result["options"]

    assert result["source_ids"] == ["SRC-001"]


def test_quiz_requires_context():

    with pytest.raises(ValueError):

        generate_quiz_question(
            competency_id="STAT.SAMPLING",
            level="L3",
            context="",
            source_ids=["SRC-001"],
        )


def test_quiz_requires_source():

    with pytest.raises(ValueError):

        generate_quiz_question(
            competency_id="STAT.SAMPLING",
            level="L3",
            context="Sampling design.",
            source_ids=[],
        )