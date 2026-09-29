from ai.recommendation.segment_recommender import (
    recommend_segments,
)


def test_sampling_l3_case_segment():

    results = recommend_segments(
        competency_id="STAT.SAMPLING",
        required_level="L3",
        evidence_dimension="CASE_DESIGN",
    )

    assert len(results) > 0

    assert (
        results[0]["resource_id"]
        == "RES-SAMPLING-002"
    )

    assert (
        results[0]["segment"]["start_seconds"]
        == 1930
    )

    assert (
        results[0]["segment"]["end_seconds"]
        == 2505
    )


def test_sampling_l4_pdf_segments():

    results = recommend_segments(
        competency_id="STAT.SAMPLING",
        required_level="L4",
        evidence_dimension="CASE_DESIGN",
    )

    assert len(results) > 0

    pages = {
        result["segment"]["page"]
        for result in results
    }

    assert 12 in pages
    assert 18 in pages


def test_no_matching_segment():

    results = recommend_segments(
        competency_id="STAT.SAMPLING",
        required_level="L4",
        evidence_dimension="UNKNOWN",
    )

    assert results == []