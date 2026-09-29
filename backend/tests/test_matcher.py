from ai.skill_extraction.matcher import match_competencies


def test_sampling_semantic_match():
    text = (
        "I can design a sampling strategy and justify "
        "the choice of sampling method."
    )

    results = match_competencies(
        text,
        top_k=3,
        threshold=0.30,
    )

    assert len(results) > 0

    competency_ids = {
        result["competency_id"]
        for result in results
    }

    assert "STAT.SAMPLING" in competency_ids


def test_empty_text_returns_empty():
    assert match_competencies("") == []