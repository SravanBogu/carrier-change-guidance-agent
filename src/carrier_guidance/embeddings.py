from openai import AzureOpenAI

from carrier_guidance.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
)


class EmbeddingClient:
    def __init__(self) -> None:
        required_settings = {
            "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
            "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
            "AZURE_OPENAI_API_VERSION": AZURE_OPENAI_API_VERSION,
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT": (
                AZURE_OPENAI_EMBEDDING_DEPLOYMENT
            ),
        }

        missing_settings = [
            name
            for name, value in required_settings.items()
            if not value
        ]

        if missing_settings:
            raise RuntimeError(
                "Missing Azure OpenAI embedding configuration: "
                + ", ".join(missing_settings)
            )

        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
        )

    def create_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            input=text,
        )

        return response.data[0].embedding