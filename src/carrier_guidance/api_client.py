from typing import Any

import httpx2 as httpx

from carrier_guidance.models import CarrierAnalysis


class CarrierIntelligenceApiError(Exception):
    """Raised when the Carrier Change Intelligence Agent API cannot be used."""


class CarrierIntelligenceApiClient:
    def __init__(self, base_url: str, timeout_seconds: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def analyze_payload(
        self,
        carrier: str,
        payload: dict[str, Any],
    ) -> CarrierAnalysis:
        try:
            response = httpx.post(
                f"{self.base_url}/analyze",
                json={
                    "carrier": carrier,
                    "payload": payload,
                },
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise CarrierIntelligenceApiError(
                "Unable to call the Carrier Change Intelligence API."
            ) from error

        try:
            return CarrierAnalysis.model_validate(response.json())
        except ValueError as error:
            raise CarrierIntelligenceApiError(
                "The Carrier Change Intelligence API returned an invalid response."
            ) from error