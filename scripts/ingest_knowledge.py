from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from carrier_guidance.chunking import chunk_markdown_file
from carrier_guidance.config import (
    AZURE_SEARCH_ADMIN_KEY,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_INDEX_NAME,
)
from carrier_guidance.embeddings import EmbeddingClient
from carrier_guidance.index_documents import to_search_document


KNOWLEDGE_DIRECTORY = Path("knowledge")


def main() -> None:
    if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_ADMIN_KEY:
        raise RuntimeError(
            "AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_ADMIN_KEY must be set."
        )

    embedding_client = EmbeddingClient()

    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY),
    )

    documents: list[dict] = []

    for path in sorted(KNOWLEDGE_DIRECTORY.glob("*.md")):
        chunks = chunk_markdown_file(path)

        for chunk in chunks:
            embedding = embedding_client.create_embedding(chunk.content)

            documents.append(
                to_search_document(
                    chunk=chunk,
                    embedding=embedding,
                )
            )

    if not documents:
        raise RuntimeError("No knowledge documents were found to ingest.")

    results = search_client.upload_documents(documents=documents)

    failed_results = [
        result
        for result in results
        if not result.succeeded
    ]

    if failed_results:
        failed_keys = ", ".join(result.key for result in failed_results)
        raise RuntimeError(
            f"Failed to upload knowledge chunks: {failed_keys}"
        )

    print(f"Uploaded {len(documents)} knowledge chunks.")


if __name__ == "__main__":
    main()