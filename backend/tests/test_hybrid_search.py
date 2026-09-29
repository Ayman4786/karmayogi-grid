from ai.retrieval.hybrid_search import hybrid_search


DOCUMENTS = [
    {
        "id": "DOC-001",
        "text": (
            "Sampling design requires selecting and "
            "justifying an appropriate sampling strategy."
        ),
    },
    {
        "id": "DOC-002",
        "text": (
            "Time series analysis covers trends, "
            "seasonality and forecasting."
        ),
    },
    {
        "id": "DOC-003",
        "text": (
            "Survey sampling methods include stratified "
            "sampling and cluster sampling."
        ),
    },
]


def test_hybrid_search_finds_sampling_content():

    results = hybrid_search(
        query="design a sampling strategy",
        documents=DOCUMENTS,
        top_k=2,
    )

    assert len(results) == 2

    ids = {
        result["id"]
        for result in results
    }

    assert "DOC-001" in ids


def test_hybrid_search_returns_scores():

    results = hybrid_search(
        query="sampling methods",
        documents=DOCUMENTS,
        top_k=3,
    )

    assert len(results) == 3

    for result in results:
        assert "semantic_score" in result
        assert "keyword_score" in result
        assert "score" in result


def test_empty_query():

    results = hybrid_search(
        query="",
        documents=DOCUMENTS,
    )

    assert results == []


def test_empty_documents():

    results = hybrid_search(
        query="sampling",
        documents=[],
    )

    assert results == []