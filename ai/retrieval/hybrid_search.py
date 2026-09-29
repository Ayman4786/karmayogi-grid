"""
Hybrid retrieval.

Combines:
1. Semantic similarity using Sentence Transformers
2. Keyword matching using BM25

The two signals are combined into a single ranking score.
"""

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_model():
    """Load the embedding model once."""

    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def hybrid_search(
    query: str,
    documents: list[dict],
    text_field: str = "text",
    top_k: int = 5,
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3,
) -> list[dict]:
    """
    Retrieve documents using semantic + keyword similarity.

    Each document must contain the field specified by text_field.
    """

    if not query or not query.strip():
        return []

    if not documents:
        return []

    texts = [
        str(document.get(text_field, ""))
        for document in documents
    ]

    # --------------------------------------------------------
    # Keyword retrieval
    # --------------------------------------------------------

    tokenized_documents = [
        text.lower().split()
        for text in texts
    ]

    bm25 = BM25Okapi(tokenized_documents)

    keyword_scores = bm25.get_scores(
        query.lower().split()
    )

    # Normalize BM25 scores to 0-1.
    max_keyword = max(keyword_scores)

    if max_keyword > 0:
        keyword_scores = [
            float(score) / max_keyword
            for score in keyword_scores
        ]
    else:
        keyword_scores = [0.0] * len(documents)

    # --------------------------------------------------------
    # Semantic retrieval
    # --------------------------------------------------------

    model = get_model()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )

    document_embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    semantic_scores = cosine_similarity(
        query_embedding,
        document_embeddings,
    )[0]

    # --------------------------------------------------------
    # Combine scores
    # --------------------------------------------------------

    results = []

    for index, document in enumerate(documents):

        semantic_score = float(
            semantic_scores[index]
        )

        keyword_score = float(
            keyword_scores[index]
        )

        combined_score = (
            semantic_weight * semantic_score
            + keyword_weight * keyword_score
        )

        results.append(
            {
                **document,
                "semantic_score": round(
                    semantic_score,
                    4,
                ),
                "keyword_score": round(
                    keyword_score,
                    4,
                ),
                "score": round(
                    combined_score,
                    4,
                ),
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]