"""
Competency framework loader and validator.

Checkpoint 0:
- Load competency framework from JSON
- Validate competency IDs
- Validate competency levels
- Validate evidence dimensions
- Detect duplicate IDs
"""

import json
from pathlib import Path


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

COMPETENCY_FILE = (
    PROJECT_ROOT
    / "data"
    / "competency_framework"
    / "competencies.json"
)


# ------------------------------------------------------------
# Allowed values
# ------------------------------------------------------------

VALID_EVIDENCE_DIMENSIONS = {
    "KNOWLEDGE",
    "APPLIED_REASONING",
    "CASE_DESIGN",
    "PRACTICAL_WORK",
}

EXPECTED_LEVELS = {"L1", "L2", "L3", "L4"}


# ------------------------------------------------------------
# Loader
# ------------------------------------------------------------

def load_competency_framework() -> dict:
    """Load the competency framework JSON file."""

    if not COMPETENCY_FILE.exists():
        raise FileNotFoundError(
            f"Competency framework not found: {COMPETENCY_FILE}"
        )

    with COMPETENCY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


# ------------------------------------------------------------
# Validator
# ------------------------------------------------------------

def validate_competency_framework(framework: dict) -> None:
    """
    Validate the competency framework.

    Raises:
        ValueError: if the framework violates Checkpoint 0 rules.
    """

    if not isinstance(framework, dict):
        raise ValueError("Framework must be a JSON object.")

    if "competencies" not in framework:
        raise ValueError("Framework must contain 'competencies'.")

    competencies = framework["competencies"]

    if not isinstance(competencies, list):
        raise ValueError("'competencies' must be a list.")

    competency_ids = set()

    for competency in competencies:

        # ----------------------------------------------------
        # Competency ID
        # ----------------------------------------------------

        competency_id = competency.get("id")

        if not competency_id:
            raise ValueError("Every competency must have an 'id'.")

        if competency_id in competency_ids:
            raise ValueError(
                f"Duplicate competency ID: {competency_id}"
            )

        competency_ids.add(competency_id)

        # ----------------------------------------------------
        # Required competency fields
        # ----------------------------------------------------

        required_fields = {
            "name",
            "domain",
            "description",
            "levels",
        }

        missing_fields = required_fields - competency.keys()

        if missing_fields:
            raise ValueError(
                f"Competency {competency_id} is missing: "
                f"{sorted(missing_fields)}"
            )

        # ----------------------------------------------------
        # Levels
        # ----------------------------------------------------

        levels = competency["levels"]

        if not isinstance(levels, list):
            raise ValueError(
                f"Levels for {competency_id} must be a list."
            )

        level_ids = set()
        level_names = set()

        for level in levels:

            level_id = level.get("id")
            level_name = level.get("level")

            if not level_id:
                raise ValueError(
                    f"Competency {competency_id} has a level "
                    "without an ID."
                )

            if level_id in level_ids:
                raise ValueError(
                    f"Duplicate level ID: {level_id}"
                )

            level_ids.add(level_id)

            if level_name in level_names:
                raise ValueError(
                    f"Duplicate level name in {competency_id}: "
                    f"{level_name}"
                )

            level_names.add(level_name)

            # ------------------------------------------------
            # Evidence dimensions
            # ------------------------------------------------

            evidence_dimensions = level.get("evidence_dimensions", [])

            invalid_dimensions = (
                set(evidence_dimensions)
                - VALID_EVIDENCE_DIMENSIONS
            )

            if invalid_dimensions:
                raise ValueError(
                    f"Invalid evidence dimensions in {level_id}: "
                    f"{sorted(invalid_dimensions)}"
                )

        # ----------------------------------------------------
        # Required prototype levels
        # ----------------------------------------------------

        actual_levels = {
            level.get("level")
            for level in levels
        }

        missing_levels = EXPECTED_LEVELS - actual_levels

        if missing_levels:
            raise ValueError(
                f"Competency {competency_id} is missing levels: "
                f"{sorted(missing_levels)}"
            )


# ------------------------------------------------------------
# Convenience function
# ------------------------------------------------------------

def load_and_validate_framework() -> dict:
    """Load the framework and validate it."""

    framework = load_competency_framework()
    validate_competency_framework(framework)

    return framework