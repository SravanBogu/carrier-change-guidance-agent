from typing import Any

from pydantic import BaseModel


class CarrierAnalysis(BaseModel):
    carrier: str
    normalized_claim: dict[str, Any]
    warnings: list[str]
    requires_human_review: bool
    message: str


class GuidanceRequest(BaseModel):
    question: str
    carrier: str
    payload: dict[str, Any]


class PreparedAgentRequest(BaseModel):
    system_instructions: str
    user_prompt: str
    analysis: CarrierAnalysis