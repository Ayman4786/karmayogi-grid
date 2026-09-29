import json
import pytest
from pathlib import Path

from ai.evaluation.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
    ndcg_at_k,
)
from ai.retrieval.hybrid_search import hybrid_search


EVALUATION_PATH = Path("data/evaluation/retrieval.json")
CATALOG_PATH = Path("data/mock_catalog/courses.json")


def load_evaluation_data():
    """Load retrieval evaluation queries."""

    with EVALUATION_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_catalog_resources():
    """Load resources from the mock catalogue."""

    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    return catalog["resources"]


def test_retrieval_evaluation_dataset_loads():
    """Evaluation dataset must contain at least one query."""

    data = load_evaluation_data()

    assert isinstance(data, list)
    assert len(data) > 0


def test_retrieval_evaluation_records_have_required_fields():
    """Every evaluation record must contain query and ground truth IDs."""

    data = load_evaluation_data()

    for record in data:
        assert "query" in record
        assert "relevant_ids" in record

        assert isinstance(record["query"], str)
        assert isinstance(record["relevant_ids"], list)


def test_evaluation_ids_exist_in_catalog():
    """Every ground-truth resource ID must exist in the catalogue."""

    resources = load_catalog_resources()

    catalog_ids = {
        resource["id"]
        for resource in resources
    }

    data = load_evaluation_data()

    for record in data:
        for resource_id in record["relevant_ids"]:
            assert resource_id in catalog_ids


def test_actual_retrieval_metrics():
    """
    Run the real hybrid retriever against every evaluation query.

    The retrieved ranking is compared against the manually defined
    relevant resource IDs.
    """

    data = load_evaluation_data()
    resources = load_catalog_resources()

    for record in data:

        results = hybrid_search(
            query=record["query"],
            documents=resources,
            text_field="description",
            top_k=3,
        )

        retrieved_ids = [
            result["id"]
            for result in results
        ]

        relevant_ids = set(
            record["relevant_ids"]
        )

        precision = precision_at_k(
            retrieved_ids=retrieved_ids,
            relevant_ids=relevant_ids,
            k=3,
        )

        recall = recall_at_k(
            retrieved_ids=retrieved_ids,
            relevant_ids=relevant_ids,
            k=3,
        )

        ndcg = ndcg_at_k(
            retrieved_ids=retrieved_ids,
            relevant_ids=relevant_ids,
            k=3,
        )

        print("\n----------------------------------------")
        print(f"Query: {record['query']}")
        print(f"Expected: {record['relevant_ids']}")
        print(f"Retrieved: {retrieved_ids}")
        print(f"Precision@3: {precision:.4f}")
        print(f"Recall@3:    {recall:.4f}")
        print(f"NDCG@3:      {ndcg:.4f}")

        assert 0.0 <= precision <= 1.0
        assert 0.0 <= recall <= 1.0
        assert 0.0 <= ndcg <= 1.0
def test_retrieval_baseline_summary():
    """
    Calculate the average retrieval metrics across the
    complete evaluation dataset.
    """

    data = load_evaluation_data()
    resources = load_catalog_resources()

    precision_scores = []
    recall_scores = []
    ndcg_scores = []

    for record in data:

        results = hybrid_search(
            query=record["query"],
            documents=resources,
            text_field="description",
            top_k=3,
        )

        retrieved_ids = [
            result["id"]
            for result in results
        ]

        relevant_ids = set(
            record["relevant_ids"]
        )

        precision_scores.append(
            precision_at_k(
                retrieved_ids,
                relevant_ids,
                k=3,
            )
        )

        recall_scores.append(
            recall_at_k(
                retrieved_ids,
                relevant_ids,
                k=3,
            )
        )

        ndcg_scores.append(
            ndcg_at_k(
                retrieved_ids,
                relevant_ids,
                k=3,
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

    average_ndcg = (
        sum(ndcg_scores)
        / len(ndcg_scores)
    )

    print("\n========================================")
    print("RETRIEVAL BASELINE")
    print("========================================")
    print(f"Queries:     {len(data)}")
    print(f"Precision@3: {average_precision:.4f}")
    print(f"Recall@3:    {average_recall:.4f}")
    print(f"NDCG@3:      {average_ndcg:.4f}")
    print("========================================")

    assert average_precision == pytest.approx(
        0.3333,
        abs=0.0001,
    )

    assert average_recall == pytest.approx(
        1.0,
        abs=0.0001,
    )

    assert average_ndcg == pytest.approx(
        0.7827,
        abs=0.0001,
    )