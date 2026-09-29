"""
Semantic competency matcher.

Uses Sentence-Transformer embeddings and cosine similarity
to map extracted learner text to controlled competencies.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ai.skill_extraction.dictionary import load_competency_dictionary


MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_model():
    """Load the embedding model once and reuse it."""

    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def match_competencies(
    text: str,
    top_k: int = 3,
    threshold: float = 0.35,
) -> list[dict]:
    """
    Match learner text against the controlled competency dictionary.

    Returns the highest-scoring competency concepts above the threshold.
    """

    if not text or not text.strip():
        return []

    dictionary = load_competency_dictionary()

    model = get_model()

    query_embedding = model.encode(
        [text],
        normalize_embeddings=True,
    )

    dictionary_texts = [
        item["text"]
        for item in dictionary
    ]

    dictionary_embeddings = model.encode(
        dictionary_texts,
        normalize_embeddings=True,
    )

    similarities = cosine_similarity(
        query_embedding,
        dictionary_embeddings,
    )[0]

    ranked = sorted(
        zip(dictionary, similarities),
        key=lambda item: item[1],
        reverse=True,
    )

    results = []

    seen_competencies = set()

    for item, score in ranked:

        competency_id = item["competency_id"]

        # Keep only the strongest match for each competency.
        if competency_id in seen_competencies:
            continue

        if score < threshold:
            continue

        seen_competencies.add(competency_id)

        results.append(
            {
                "competency_id": competency_id,
                "level": item.get("level"),
                "level_id": item.get("level_id"),
                "matched_text": item["text"],
                "similarity": round(float(score), 4),
            }
        )

        if len(results) >= top_k:
            break

    return results