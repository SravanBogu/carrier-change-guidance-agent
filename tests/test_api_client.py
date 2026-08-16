from unittest.mock import patch

import httpx2 as httpx
import pytest

from carrier_guidance.api_client import (
    CarrierIntelligenceApiClient,
    CarrierIntelligenceApiError,
)


def test_analyze_payload_returns_typed_api_response() -> None:
    request = httpx.Request(
        method="POST",
        url="http://127.0.0.1:8000/analyze",
    )

    response = httpx.Response(
        status_code=200,
        request=request,
        json={
            "carrier": "Northwind Mutual",
            "normalized_claim": {
                "carrier": "Northwind Mutual",
                "claim_id": "C-1001",
                "policy_number": None,
                "date_of_loss": None,
                "date_reported": None,
                "loss_type": None,
            },
            "warnings": ["Unmapped source field: lossOccurredWhen"],
            "requires_human_review": True,
            "message": (
                "Carrier payload normalized with warnings "
                "and requires human review."
            ),
        },
    )

    with patch("carrier_guidance.api_client.httpx.post", return_value=response):
        client = CarrierIntelligenceApiClient(
            base_url="http://127.0.0.1:8000",
        )

        analysis = client.analyze_payload(
            carrier="Northwind Mutual",
            payload={"lossOccurredWhen": "2026-07-30"},
        )

    assert analysis.requires_human_review is True
    assert analysis.warnings == ["Unmapped source field: lossOccurredWhen"]
    assert analysis.normalized_claim["claim_id"] == "C-1001"


def test_analyze_payload_wraps_http_error() -> None:
    request = httpx.Request(
        method="POST",
        url="http://127.0.0.1:8000/analyze",
    )

    response = httpx.Response(
        status_code=503,
        request=request,
    )

    with patch("carrier_guidance.api_client.httpx.post", return_value=response):
        client = CarrierIntelligenceApiClient(
            base_url="http://127.0.0.1:8000",
        )

        with pytest.raises(
            CarrierIntelligenceApiError,
            match="Unable to call the Carrier Change Intelligence API.",
        ):
            client.analyze_payload(
                carrier="Northwind Mutual",
                payload={"claimId": "C-1001"},
            )