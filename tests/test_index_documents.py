from carrier_guidance.index_documents import to_search_document
from carrier_guidance.retrieval_models import KnowledgeChunk


def test_to_search_document_preserves_chunk_metadata() -> None:
    chunk = KnowledgeChunk(
        chunk_id="claims-intake-policy-002",
        title="Claims Intake Policy",
        content="Unknown fields require human review.",
        source_file="claims-intake-policy.md",
        section="Unknown source fields",
        chunk_index=2,
    )

    document = to_search_document(
        chunk=chunk,
        embedding=[0.1, 0.2, 0.3],
    )

    assert document["id"] == "claims-intake-policy-002"
    assert document["content_vector"] == [0.1, 0.2, 0.3]
    assert document["source_file"] == "claims-intake-policy.md"