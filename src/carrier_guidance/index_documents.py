from carrier_guidance.retrieval_models import KnowledgeChunk


def to_search_document(
    chunk: KnowledgeChunk,
    embedding: list[float],
) -> dict:
    return {
        "id": chunk.chunk_id,
        "title": chunk.title,
        "content": chunk.content,
        "content_vector": embedding,
        "source_file": chunk.source_file,
        "section": chunk.section,
        "chunk_index": chunk.chunk_index,
    }