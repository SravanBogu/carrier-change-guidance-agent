from carrier_guidance.retrieval_models import RetrievedSource
from carrier_guidance.retrieval_policy import decide_retrieval_sufficiency


def test_no_sources_returns_insufficient_retrieval() -> None:
    decision = decide_retrieval_sufficiency([])

    assert decision.grounded is False
    assert decision.retrieval_status == "insufficient"
    assert decision.sources == []


def test_usable_source_returns_sufficient_retrieval() -> None:
    source = RetrievedSource(
        chunk_id="claims-intake-policy-002",
        title="Claims Intake Policy",
        content="Unknown source fields require human review.",
        source_file="claims-intake-policy.md",
        section="Unknown source fields",
        search_score=1.2,
        reranker_score=2.4,
    )

    decision = decide_retrieval_sufficiency([source])

    assert decision.grounded is True
    assert decision.retrieval_status == "sufficient"
    assert decision.sources == [source]


def test_source_without_metadata_returns_insufficient_retrieval() -> None:
    source = RetrievedSource(
        chunk_id="missing-metadata-001",
        title="Carrier Policy",
        content="Known policy content.",
        source_file="",
        section="",
    )

    decision = decide_retrieval_sufficiency([source])

    assert decision.grounded is False
    assert decision.retrieval_status == "insufficient"