from pydantic import BaseModel, Field


class CapabilityEvaluationRequest(BaseModel):
    required_level: str = Field(
        ...,
        pattern=r"^L[1-4]$",
    )

    evidence_dimensions: dict[str, float] = Field(
        default_factory=dict,
    )


class CapabilityEvaluationResponse(BaseModel):
    capability: dict
    evidence_status: dict
    gap: dict
    next_best_evidence: dict