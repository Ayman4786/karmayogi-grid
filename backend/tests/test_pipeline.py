from ai.rag.pipeline import build_rag_context
from ai.rag.prompt_builder import build_grounded_prompt


DOCUMENTS = [
    {
        "id": "SRC-001",
        "text": (
            "Stratified sampling divides the population into "
            "subgroups and samples from each subgroup."
        ),
    },
    {
        "id": "SRC-002",
        "text": (
            "Cluster sampling selects groups or clusters "
            "rather than individual units."
        ),
    },
    {
        "id": "SRC-003",
        "text": (
            "Time series analysis studies observations "
            "collected over time."
        ),
    },
]


def test_rag_retrieves_grounded_context():

    result = build_rag_context(
        query="Explain stratified sampling.",
        documents=DOCUMENTS,
        top_k=2,
    )

    assert result["grounded"] is True
    assert len(result["sources"]) == 2
    assert "SRC-001" in result["context"]


def test_empty_retrieval_is_not_grounded():

    result = build_rag_context(
        query="",
        documents=DOCUMENTS,
    )

    assert result["grounded"] is False
    assert result["context"] == ""


def test_grounded_prompt_contains_context():

    prompt = build_grounded_prompt(
        question_task="Create one assessment question.",
        context="Stratified sampling divides a population into subgroups.",
    )

    assert "SOURCE CONTEXT" in prompt
    assert "Stratified sampling" in prompt
    assert "assessment question" in prompt