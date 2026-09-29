"""
Exact learning-resource segment recommender.

Returns the most relevant timestamp/page segment from a
resource catalogue for a competency and evidence dimension.
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CATALOG_FILE = (
    PROJECT_ROOT
    / "data"
    / "mock_catalog"
    / "courses.json"
)


def load_resource_catalog() -> dict:
    """Load the mock learning-resource catalogue."""

    with CATALOG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def recommend_segments(
    competency_id: str,
    required_level: str,
    evidence_dimension: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Find exact resource segments relevant to the requirement.
    """

    catalog = load_resource_catalog()
    results = []

    for resource in catalog["resources"]:

        if competency_id not in resource.get("competency_ids", []):
            continue

        if required_level not in resource.get("levels", []):
            continue

        if evidence_dimension not in resource.get(
            "evidence_dimensions", []
        ):
            continue

        for segment in resource.get("segments", []):

            results.append(
                {
                    "resource_id": resource["id"],
                    "resource_title": resource["title"],
                    "source_type": resource["source_type"],
                    "segment": segment,
                }
            )

    return results[:top_k]