from carrier_guidance.api_client import CarrierIntelligenceApiClient
from carrier_guidance.config import CARRIER_INTELLIGENCE_API_BASE_URL
from carrier_guidance.models import GuidanceRequest
from carrier_guidance.prompts import build_agent_request


def main() -> None:
    request = GuidanceRequest(
        question="What should happen to this payload?",
        carrier="Northwind Mutual",
        payload={
            "claimId": "C-1001",
            "lossOccurredWhen": "2026-07-30",
        },
    )

    client = CarrierIntelligenceApiClient(
        base_url=CARRIER_INTELLIGENCE_API_BASE_URL,
    )

    analysis = client.analyze_payload(
        carrier=request.carrier,
        payload=request.payload,
    )

    prepared_request = build_agent_request(
        question=request.question,
        analysis=analysis,
    )

    print("Carrier Change Intelligence Agent API result:")
    print(analysis.model_dump_json(indent=2))
    print("\nPrepared Foundry system instructions:")
    print(prepared_request.system_instructions)
    print("\nPrepared Foundry user prompt:")
    print(prepared_request.user_prompt)


if __name__ == "__main__":
    main()