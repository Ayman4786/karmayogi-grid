from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_generate_assessment():
    """Assessment endpoint should generate a valid MCQ."""

    response = client.post(
        "/assessment/generate",
        json={
            "competency_id": "STAT.SAMPLING",
            "level": "L3",
            "context": (
                "Sampling design requires selecting and "
                "justifying an appropriate sampling strategy."
            ),
            "source_ids": [
                "RES-SAMPLING-002",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "question" in data

    question = data["question"]

    assert question["competency_id"] == "STAT.SAMPLING"
    assert question["level"] == "L3"
    assert len(question["options"]) == 4
    assert question["correct_answer"] in question["options"]
    assert question["source_ids"] == [
        "RES-SAMPLING-002",
    ]
    assert question["evidence_dimension"] == "KNOWLEDGE"


def test_submit_correct_assessment_answer():
    """Correct MCQ answer should produce full assessment score."""

    question = {
        "question": (
            "Which approach is most appropriate?"
        ),
        "options": [
            "Select and justify an appropriate approach.",
            "Memorize terminology.",
            "Ignore the problem characteristics.",
            "Use the same approach every time.",
        ],
        "correct_answer": (
            "Select and justify an appropriate approach."
        ),
        "explanation": (
            "The approach should be selected based "
            "on the problem."
        ),
        "competency_id": "STAT.SAMPLING",
        "level": "L3",
        "source_ids": [
            "RES-SAMPLING-002",
        ],
        "evidence_dimension": "KNOWLEDGE",
    }

    response = client.post(
        "/assessment/submit",
        json={
            "question": question,
            "answer": (
                "Select and justify an appropriate approach."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["score"]["score"] == 1.0
    assert data["score"]["correct_answers"] == 1

    assert data["evidence"]["dimension"] == "KNOWLEDGE"
    assert data["evidence"]["score"] == 1.0


def test_submit_incorrect_assessment_answer():
    """Incorrect MCQ answer should produce zero score."""

    question = {
        "question": (
            "Which approach is most appropriate?"
        ),
        "options": [
            "Select and justify an appropriate approach.",
            "Memorize terminology.",
            "Ignore the problem characteristics.",
            "Use the same approach every time.",
        ],
        "correct_answer": (
            "Select and justify an appropriate approach."
        ),
        "explanation": (
            "The approach should be selected based "
            "on the problem."
        ),
        "competency_id": "STAT.SAMPLING",
        "level": "L3",
        "source_ids": [
            "RES-SAMPLING-002",
        ],
        "evidence_dimension": "KNOWLEDGE",
    }

    response = client.post(
        "/assessment/submit",
        json={
            "question": question,
            "answer": "Memorize terminology.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["score"]["score"] == 0.0
    assert data["score"]["correct_answers"] == 0


def test_assessment_produces_evidence_not_direct_capability():
    """
    A single MCQ should produce knowledge evidence.

    It should not automatically claim that the learner
    achieved the requested competency level.
    """

    question = {
        "question": (
            "Which approach is most appropriate?"
        ),
        "options": [
            "Select and justify an appropriate approach.",
            "Memorize terminology.",
            "Ignore the problem characteristics.",
            "Use the same approach every time.",
        ],
        "correct_answer": (
            "Select and justify an appropriate approach."
        ),
        "explanation": (
            "The approach should be selected based "
            "on the problem."
        ),
        "competency_id": "STAT.SAMPLING",
        "level": "L3",
        "source_ids": [
            "RES-SAMPLING-002",
        ],
        "evidence_dimension": "KNOWLEDGE",
    }

    response = client.post(
        "/assessment/submit",
        json={
            "question": question,
            "answer": (
                "Select and justify an appropriate approach."
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["evidence"]["dimension"] == "KNOWLEDGE"

    # A single MCQ provides only knowledge evidence.
    # The remaining dimensions are unknown, so capability
    # cannot yet be established.
    assert data["evidence_status"]["status"] == "UNKNOWN"