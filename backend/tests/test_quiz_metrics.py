import pytest

from ai.evaluation.quiz_metrics import (
    answer_precision,
    answer_recall,
    answer_f1,
    groundedness,
)


def test_answer_precision_full_match():
    score = answer_precision(
        expected_answer="stratified sampling",
        generated_answer="stratified sampling",
    )

    assert score == pytest.approx(1.0)


def test_answer_precision_partial_match():
    score = answer_precision(
        expected_answer="stratified sampling",
        generated_answer="stratified method",
    )

    assert score == pytest.approx(0.5)


def test_answer_recall_full_match():
    score = answer_recall(
        expected_answer="stratified sampling",
        generated_answer="stratified sampling",
    )

    assert score == pytest.approx(1.0)


def test_answer_recall_partial_match():
    score = answer_recall(
        expected_answer="stratified sampling",
        generated_answer="stratified method",
    )

    assert score == pytest.approx(0.5)


def test_answer_f1_full_match():
    score = answer_f1(
        expected_answer="stratified sampling",
        generated_answer="stratified sampling",
    )

    assert score == pytest.approx(1.0)


def test_answer_f1_no_match():
    score = answer_f1(
        expected_answer="stratified sampling",
        generated_answer="cluster design",
    )

    assert score == pytest.approx(0.0)


def test_groundedness_full_match():
    score = groundedness(
        expected_source_ids=["RES-SAMPLING-002"],
        generated_source_ids=["RES-SAMPLING-002"],
    )

    assert score == pytest.approx(1.0)


def test_groundedness_partial_match():
    score = groundedness(
        expected_source_ids=[
            "RES-SAMPLING-002",
            "RES-SAMPLING-004",
        ],
        generated_source_ids=[
            "RES-SAMPLING-002",
        ],
    )

    assert score == pytest.approx(0.5)


def test_groundedness_no_match():
    score = groundedness(
        expected_source_ids=["RES-SAMPLING-002"],
        generated_source_ids=["RES-SAMPLING-001"],
    )

    assert score == pytest.approx(0.0)