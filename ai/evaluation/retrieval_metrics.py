from math import log2


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Measure how many of the top-k retrieved items are relevant."""

    if k <= 0:
        raise ValueError("k must be greater than 0")

    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(
        1 for item_id in retrieved
        if item_id in relevant_ids
    )

    return relevant_count / len(retrieved)


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Measure how many relevant items were found in the top-k results."""

    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not relevant_ids:
        return 0.0

    retrieved = retrieved_ids[:k]

    relevant_count = sum(
        1 for item_id in retrieved
        if item_id in relevant_ids
    )

    return relevant_count / len(relevant_ids)


def ndcg_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    """Measure ranking quality of the top-k results."""

    if k <= 0:
        raise ValueError("k must be greater than 0")

    retrieved = retrieved_ids[:k]

    if not retrieved or not relevant_ids:
        return 0.0

    # Binary relevance:
    # relevant item = 1
    # non-relevant item = 0
    dcg = 0.0

    for rank, item_id in enumerate(retrieved, start=1):
        relevance = 1 if item_id in relevant_ids else 0

        if relevance:
            dcg += relevance / log2(rank + 1)

    # Ideal ranking puts all relevant items first.
    ideal_count = min(k, len(relevant_ids))

    idcg = sum(
        1 / log2(rank + 1)
        for rank in range(1, ideal_count + 1)
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg