import json
from pathlib import Path

from ai.evaluation.quiz_metrics import (
    answer_precision,
    answer_recall,
    answer_f1,
    groundedness,
)
from ai.quiz.generator import generate_quiz_question


EVALUATION_PATH = Path("data/evaluation/quiz.json")


def load_quiz_evaluation_data():
    """Load the prototype quiz evaluation dataset."""

    with EVALUATION_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_quiz_evaluation_dataset_loads():
    """Evaluation dataset must contain at least one record."""

    data = load_quiz_evaluation_data()

    assert isinstance(data, list)
    assert len(data) > 0


def test_quiz_evaluation_records_have_required_fields():
    """Every evaluation record must contain required fields."""

    data = load_quiz_evaluation_data()

    for record in data:
        assert "question_id" in record
        assert "competency_id" in record
        assert "level" in record
        assert "expected_answer" in record
        assert "source_ids" in record

        assert isinstance(record["question_id"], str)
        assert isinstance(record["competency_id"], str)
        assert isinstance(record["level"], str)
        assert isinstance(record["expected_answer"], str)
        assert isinstance(record["source_ids"], list)


def test_actual_quiz_evaluation_metrics():
    """
    Generate assessment content and calculate AI evaluation metrics.

    The generated assessment is compared against the prototype
    evaluation dataset.
    """

    data = load_quiz_evaluation_data()

    for record in data:

        generated = generate_quiz_question(
            competency_id=record["competency_id"],
            level=record["level"],
            context=(
                f"Source {record['source_ids'][0]}: "
                f"{record['expected_answer']}"
            ),
            source_ids=record["source_ids"],
        )

        generated_answer = generated["correct_answer"]

        precision = answer_precision(
            record["expected_answer"],
            generated_answer,
        )

        recall = answer_recall(
            record["expected_answer"],
            generated_answer,
        )

        f1 = answer_f1(
            record["expected_answer"],
            generated_answer,
        )

        grounding = groundedness(
            record["source_ids"],
            generated["source_ids"],
        )

        print("\n----------------------------------------")
        print(f"Question:     {record['question_id']}")
        print(f"Competency:   {record['competency_id']}")
        print(f"Level:        {record['level']}")
        print(f"Expected:     {record['expected_answer']}")
        print(f"Generated:    {generated_answer}")
        print(f"Precision:    {precision:.4f}")
        print(f"Recall:       {recall:.4f}")
        print(f"F1:           {f1:.4f}")
        print(f"Groundedness: {grounding:.4f}")

        assert 0.0 <= precision <= 1.0
        assert 0.0 <= recall <= 1.0
        assert 0.0 <= f1 <= 1.0
        assert 0.0 <= grounding <= 1.0

def test_quiz_evaluation_baseline_summary():
    """
    Calculate average AI evaluation metrics across
    the complete evaluation dataset.
    """

    data = load_quiz_evaluation_data()

    precision_scores = []
    recall_scores = []
    f1_scores = []
    groundedness_scores = []

    for record in data:

        generated = generate_quiz_question(
            competency_id=record["competency_id"],
            level=record["level"],
            context=(
                f"Source {record['source_ids'][0]}: "
                f"{record['expected_answer']}"
            ),
            source_ids=record["source_ids"],
        )

        generated_answer = generated["correct_answer"]

        precision_scores.append(
            answer_precision(
                record["expected_answer"],
                generated_answer,
            )
        )

        recall_scores.append(
            answer_recall(
                record["expected_answer"],
                generated_answer,
            )
        )

        f1_scores.append(
            answer_f1(
                record["expected_answer"],
                generated_answer,
            )
        )

        groundedness_scores.append(
            groundedness(
                record["source_ids"],
                generated["source_ids"],
            )
        )

    average_precision = (
        sum(precision_scores)
        / len(precision_scores)
    )

    average_recall = (
        sum(recall_scores)
        / len(recall_scores)
    )

    average_f1 = (
        sum(f1_scores)
        / len(f1_scores)
    )

    average_groundedness = (
        sum(groundedness_scores)
        / len(groundedness_scores)
    )

    print("\n========================================")
    print("AI ASSESSMENT BASELINE")
    print("========================================")
    print(f"Questions:     {len(data)}")
    print(f"Precision:     {average_precision:.4f}")
    print(f"Recall:        {average_recall:.4f}")
    print(f"F1:            {average_f1:.4f}")
    print(f"Groundedness:  {average_groundedness:.4f}")
    print("========================================")

    assert 0.0 <= average_precision <= 1.0
    assert 0.0 <= average_recall <= 1.0
    assert 0.0 <= average_f1 <= 1.0
    assert 0.0 <= average_groundedness <= 1.0