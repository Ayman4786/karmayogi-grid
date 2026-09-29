"""
Controlled competency dictionary.

This file provides the concepts used by the skill extraction
and competency matching pipeline.

The competency framework JSON remains the source of truth.
This dictionary provides searchable concepts derived from it.
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

COMPETENCY_FILE = (
    PROJECT_ROOT
    / "data"
    / "competency_framework"
    / "competencies.json"
)


def load_competency_dictionary() -> list[dict]:
    """
    Load competencies and convert them into searchable concepts.
    """

    with COMPETENCY_FILE.open("r", encoding="utf-8") as file:
        framework = json.load(file)

    dictionary = []

    for competency in framework["competencies"]:
        competency_id = competency["id"]

        # Base competency concept
        dictionary.append(
            {
                "competency_id": competency_id,
                "level": None,
                "text": competency["name"],
            }
        )

        # Add descriptions and level-specific concepts
        for level in competency["levels"]:
            level_id = level["id"]
            level_name = level["level"]

            for field in (
                "learning_objectives",
                "knowledge_indicators",
                "observable_behaviours",
            ):
                for item in level.get(field, []):
                    dictionary.append(
                        {
                            "competency_id": competency_id,
                            "level": level_name,
                            "level_id": level_id,
                            "text": item,
                        }
                    )

    return dictionary