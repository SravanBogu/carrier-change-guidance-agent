from pydantic import BaseModel, Field


class KnowledgeChunk(BaseModel):
    chunk_id: str
    title: str
    content: str
    source_file: str
    section: str
    chunk_index: int


class RetrievedSource(BaseModel):
    chunk_id: str
    title: str
    content: str
    source_file: str
    section: str
    search_score: float | None = None
    reranker_score: float | None = None


class RetrievalDecision(BaseModel):
    grounded: bool
    retrieval_status: str
    reason: str
    sources: list[RetrievedSource] = Field(default_factory=list)