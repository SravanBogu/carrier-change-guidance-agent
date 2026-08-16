import json

from carrier_guidance.models import CarrierAnalysis, PreparedAgentRequest


SYSTEM_INSTRUCTIONS = """
You are the Carrier Change Guidance Agent.

The Carrier Change Intelligence Agent API is authoritative for canonical claim data,
processing warnings, and requires_human_review.

Use approved knowledge sources only to explain carrier field mappings,
validation requirements, and human-review policy.

Do not infer unknown source-field mappings.
Do not modify canonical claim data.
Do not override requires_human_review.
Do not approve, deny, or adjudicate claims.

If approved knowledge does not support an answer, reply exactly:
"I do not have sufficient approved information to answer that.
Please route this item for human review."

When sources support an answer, identify the relevant source title and section.
All examples are synthetic demonstration data.
""".strip()


def build_agent_request(
    question: str,
    analysis: CarrierAnalysis,
) -> PreparedAgentRequest:
    user_prompt = (
        "User question:\n"
        f"{question}\n\n"
        "Authoritative API analysis:\n"
        f"{json.dumps(analysis.model_dump(), indent=2)}\n\n"
        "Explain the result using approved knowledge sources only. "
        "Preserve the API human-review decision."
    )

    return PreparedAgentRequest(
        system_instructions=SYSTEM_INSTRUCTIONS,
        user_prompt=user_prompt,
        analysis=analysis,
    )