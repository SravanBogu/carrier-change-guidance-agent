from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from carrier_guidance.config import (
    AZURE_SEARCH_ADMIN_KEY,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_INDEX_NAME,
)
from carrier_guidance.embeddings import EmbeddingClient
from carrier_guidance.retrieval_models import RetrievedSource


class CarrierGuidanceSearchClient:
    def __init__(self) -> None:
        if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_ADMIN_KEY:
            raise RuntimeError(
                "AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_ADMIN_KEY must be set."
            )

        self.embedding_client = EmbeddingClient()
        self.search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY),
        )

    def hybrid_search(
        self,
        query: str,
        top: int = 3,
    ) -> list[RetrievedSource]:
        vector = self.embedding_client.create_embedding(query)

        vector_query = VectorizedQuery(
            vector=vector,
            k_nearest_neighbors=top,
            fields="content_vector",
        )

        results = self.search_client.search(
            search_text=query,
            vector_queries=[vector_query],
            top=top,
            select=[
                "id",
                "title",
                "content",
                "source_file",
                "section",
            ],
        )

        return [
            RetrievedSource(
                chunk_id=result["id"],
                title=result["title"],
                content=result["content"],
                source_file=result["source_file"],
                section=result["section"],
                search_score=result.get("@search.score"),
                reranker_score=result.get("@search.reranker_score"),
            )
            for result in results
        ]