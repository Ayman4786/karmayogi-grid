from pydantic import BaseModel, Field


class AssessmentGenerateRequest(BaseModel):
    competency_id: str

    level: str = Field(
        ...,
        pattern=r"^L[1-4]$",
    )

    context: str
    source_ids: list[str]


class AssessmentGenerateResponse(BaseModel):
    question: dict


class AssessmentSubmitRequest(BaseModel):
    question: dict
    answer: str


class AssessmentSubmitResponse(BaseModel):
    score: dict
    evidence: dict
    capability: dict
    evidence_status: dict
    gap: dict
    next_best_evidence: dict