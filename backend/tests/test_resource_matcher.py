from ai.recommendation.resource_matcher import (
    match_learning_resources,
)


RESOURCES = [
    {
        "id": "RES-001",
        "title": "Sampling Fundamentals",
        "competency_ids": ["STAT.SAMPLING"],
        "levels": ["L1", "L2"],
        "evidence_dimensions": ["KNOWLEDGE"],
    },
    {
        "id": "RES-002",
        "title": "Sampling Design Case Study",
        "competency_ids": ["STAT.SAMPLING"],
        "levels": ["L3"],
        "evidence_dimensions": ["CASE_DESIGN"],
    },
    {
        "id": "RES-003",
        "title": "General Statistics",
        "competency_ids": ["STAT.OTHER"],
        "levels": ["L3"],
        "evidence_dimensions": ["KNOWLEDGE"],
    },
]


def test_resource_matching():

    results = match_learning_resources(
        competency_id="STAT.SAMPLING",
        required_level="L3",
        resources=RESOURCES,
        evidence_dimension="CASE_DESIGN",
    )

    assert len(results) > 0
    assert results[0]["id"] == "RES-002"


def test_unrelated_resource_is_not_top_match():

    results = match_learning_resources(
        competency_id="STAT.SAMPLING",
        required_level="L3",
        resources=RESOURCES,
    )

    assert results[0]["id"] != "RES-003"


def test_top_k():

    results = match_learning_resources(
        competency_id="STAT.SAMPLING",
        required_level="L3",
        resources=RESOURCES,
        top_k=1,
    )

    assert len(results) == 1