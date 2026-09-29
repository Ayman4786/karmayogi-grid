"""
Metrics for evaluating AI-generated assessment content.

The prototype evaluates four things:

1. Precision
2. Recall
3. F1
4. Groundedness

Precision, recall, and F1 are calculated using token overlap
between the expected answer and generated answer.

Groundedness measures whether the generated assessment cites
the expected source resources.
"""


def _tokenize(text: str) -> set[str]:
    """Convert text into a normalized set of tokens."""

    if not text:
        return set()

    return {
        token.strip(".,!?;:()[]{}\"'")
        for token in text.lower().split()
        if token.strip(".,!?;:()[]{}\"'")
    }


def answer_precision(
    expected_answer: str,
    generated_answer: str,
) -> float:
    """
    Measure how much of the generated answer overlaps
    with the expected answer.
    """

    expected_tokens = _tokenize(expected_answer)
    generated_tokens = _tokenize(generated_answer)

    if not generated_tokens:
        return 0.0

    overlap = expected_tokens & generated_tokens

    return len(overlap) / len(generated_tokens)


def answer_recall(
    expected_answer: str,
    generated_answer: str,
) -> float:
    """
    Measure how much of the expected answer is covered
    by the generated answer.
    """

    expected_tokens = _tokenize(expected_answer)
    generated_tokens = _tokenize(generated_answer)

    if not expected_tokens:
        return 0.0

    overlap = expected_tokens & generated_tokens

    return len(overlap) / len(expected_tokens)


def answer_f1(
    expected_answer: str,
    generated_answer: str,
) -> float:
    """Calculate F1 from answer precision and recall."""

    precision = answer_precision(
        expected_answer,
        generated_answer,
    )

    recall = answer_recall(
        expected_answer,
        generated_answer,
    )

    if precision + recall == 0:
        return 0.0

    return (
        2 * precision * recall
        / (precision + recall)
    )


def groundedness(
    expected_source_ids: list[str],
    generated_source_ids: list[str],
) -> float:
    """
    Measure how much the generated content is grounded
    in the expected source resources.

    A score of 1.0 means all expected sources are present.
    A score of 0.0 means none are present.
    """

    expected_sources = set(expected_source_ids)
    generated_sources = set(generated_source_ids)

    if not expected_sources:
        return 0.0

    matched_sources = (
        expected_sources & generated_sources
    )

    return len(matched_sources) / len(expected_sources)