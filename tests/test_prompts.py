from carrier_guidance.models import CarrierAnalysis
from carrier_guidance.prompts import build_agent_request


def test_build_agent_request_preserves_api_review_decision() -> None:
    analysis = CarrierAnalysis(
        carrier="Northwind Mutual",
        normalized_claim={
            "carrier": "Northwind Mutual",
            "date_of_loss": None,
        },
        warnings=["Unmapped source field: lossOccurredWhen"],
        requires_human_review=True,
        message="Carrier payload normalized with warnings and requires human review.",
    )

    prepared = build_agent_request(
        question="What should happen to this payload?",
        analysis=analysis,
    )

    assert prepared.analysis.requires_human_review is True
    assert "lossOccurredWhen" in prepared.user_prompt
    assert "Do not infer unknown source-field mappings." in prepared.system_instructions