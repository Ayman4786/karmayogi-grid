"""
Tests for the competency framework.

Checkpoint 0:
- Framework loads successfully
- Framework structure is valid
- Competencies have required levels
- Evidence dimensions are valid
- Duplicate IDs are rejected
"""

import pytest

from backend.app.services.competency_service import (
    load_and_validate_framework,
    validate_competency_framework,
)


def test_competency_framework_loads():
    """The competency framework should load and validate successfully."""

    framework = load_and_validate_framework()

    assert framework is not None
    assert "competencies" in framework
    assert len(framework["competencies"]) > 0


def test_sampling_competency_exists():
    """The prototype Sampling competency should exist."""

    framework = load_and_validate_framework()

    competency_ids = {
        competency["id"]
        for competency in framework["competencies"]
    }

    assert "STAT.SAMPLING" in competency_ids


def test_sampling_has_all_levels():
    """Sampling should contain L1, L2, L3 and L4."""

    framework = load_and_validate_framework()

    sampling = next(
        competency
        for competency in framework["competencies"]
        if competency["id"] == "STAT.SAMPLING"
    )

    levels = {
        level["level"]
        for level in sampling["levels"]
    }

    assert levels == {"L1", "L2", "L3", "L4"}


def test_invalid_evidence_dimension_is_rejected():
    """Unknown evidence dimensions should fail validation."""

    framework = {
        "competencies": [
            {
                "id": "TEST.COMPETENCY",
                "name": "Test",
                "domain": "Testing",
                "description": "Test competency",
                "levels": [
                    {
                        "id": "TEST.COMPETENCY.L1",
                        "level": "L1",
                        "evidence_dimensions": [
                            "INVALID_DIMENSION"
                        ],
                    },
                    {
                        "id": "TEST.COMPETENCY.L2",
                        "level": "L2",
                        "evidence_dimensions": [],
                    },
                    {
                        "id": "TEST.COMPETENCY.L3",
                        "level": "L3",
                        "evidence_dimensions": [],
                    },
                    {
                        "id": "TEST.COMPETENCY.L4",
                        "level": "L4",
                        "evidence_dimensions": [],
                    },
                ],
            }
        ]
    }

    with pytest.raises(ValueError):
        validate_competency_framework(framework)


def test_duplicate_competency_id_is_rejected():
    """Duplicate competency IDs should fail validation."""

    framework = {
        "competencies": [
            {
                "id": "TEST.COMPETENCY",
                "name": "Test 1",
                "domain": "Testing",
                "description": "Test competency",
                "levels": [
                    {"id": "T1.L1", "level": "L1", "evidence_dimensions": []},
                    {"id": "T1.L2", "level": "L2", "evidence_dimensions": []},
                    {"id": "T1.L3", "level": "L3", "evidence_dimensions": []},
                    {"id": "T1.L4", "level": "L4", "evidence_dimensions": []},
                ],
            },
            {
                "id": "TEST.COMPETENCY",
                "name": "Test 2",
                "domain": "Testing",
                "description": "Duplicate competency",
                "levels": [
                    {"id": "T2.L1", "level": "L1", "evidence_dimensions": []},
                    {"id": "T2.L2", "level": "L2", "evidence_dimensions": []},
                    {"id": "T2.L3", "level": "L3", "evidence_dimensions": []},
                    {"id": "T2.L4", "level": "L4", "evidence_dimensions": []},
                ],
            },
        ]
    }

    with pytest.raises(ValueError):
        validate_competency_framework(framework)