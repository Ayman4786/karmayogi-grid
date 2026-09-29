from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_capability_evaluation_endpoint():
    """Capability evaluation endpoint should return structured results."""

    response = client.post(
        "/capability/evaluate",
        json={
            "required_level": "L3",
            "evidence_dimensions": {
                "KNOWLEDGE": 0.8,
                "APPLIED_REASONING": 0.7,
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "capability" in data
    assert "evidence_status" in data
    assert "gap" in data
    assert "next_best_evidence" in data


def test_capability_evaluation_rejects_invalid_level():
    """Capability evaluation should reject invalid competency levels."""

    response = client.post(
        "/capability/evaluate",
        json={
            "required_level": "L5",
            "evidence_dimensions": {},
        },
    )

    assert response.status_code == 422