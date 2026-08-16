from carrier_guidance.retrieval_models import (
    RetrievalDecision,
    RetrievedSource,
)


SAFE_FALLBACK = (
    "I do not have sufficient approved information to answer that. "
    "Please route this item for human review."
)


def decide_retrieval_sufficiency(
    sources: list[RetrievedSource],
) -> RetrievalDecision:
    if not sources:
        return RetrievalDecision(
            grounded=False,
            retrieval_status="insufficient",
            reason="No approved knowledge sources were retrieved.",
            sources=[],
        )

    usable_sources = [
        source
        for source in sources
        if source.content.strip()
        and source.source_file.strip()
        and source.section.strip()
    ]

    if not usable_sources:
        return RetrievalDecision(
            grounded=False,
            retrieval_status="insufficient",
            reason="Retrieved sources did not contain usable citation metadata.",
            sources=[],
        )

    return RetrievalDecision(
        grounded=True,
        retrieval_status="sufficient",
        reason="Approved knowledge sources were retrieved with usable metadata.",
        sources=usable_sources,
    )