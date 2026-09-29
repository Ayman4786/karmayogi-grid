import pytest

from ai.evaluation.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
    ndcg_at_k,
)


RETRIEVED = ["A", "B", "C", "D"]
RELEVANT = {"A", "C"}


def test_precision_at_k():
    result = precision_at_k(
        retrieved_ids=RETRIEVED,
        relevant_ids=RELEVANT,
        k=4,
    )

    assert result == 0.5


def test_recall_at_k():
    result = recall_at_k(
        retrieved_ids=RETRIEVED,
        relevant_ids=RELEVANT,
        k=2,
    )

    assert result == 0.5


def test_recall_finds_all_relevant_items():
    result = recall_at_k(
        retrieved_ids=RETRIEVED,
        relevant_ids=RELEVANT,
        k=4,
    )

    assert result == 1.0


def test_ndcg_at_k():
    result = ndcg_at_k(
        retrieved_ids=["A", "B", "C"],
        relevant_ids={"A", "C"},
        k=3,
    )

    assert 0.0 < result < 1.0


def test_perfect_ndcg():
    result = ndcg_at_k(
        retrieved_ids=["A", "C", "B"],
        relevant_ids={"A", "C"},
        k=2,
    )

    assert result == pytest.approx(1.0)


def test_invalid_k_is_rejected():
    with pytest.raises(ValueError):
        precision_at_k(
            retrieved_ids=RETRIEVED,
            relevant_ids=RELEVANT,
            k=0,
        )


def test_empty_retrieval():
    assert (
        precision_at_k(
            retrieved_ids=[],
            relevant_ids=RELEVANT,
            k=3,
        )
        == 0.0
    )


def test_empty_relevant_set():
    assert (
        recall_at_k(
            retrieved_ids=RETRIEVED,
            relevant_ids=set(),
            k=3,
        )
        == 0.0
    )