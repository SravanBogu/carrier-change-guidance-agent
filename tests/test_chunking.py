from pathlib import Path

from carrier_guidance.chunking import chunk_markdown_file


def test_chunk_markdown_file_preserves_source_metadata(
    tmp_path: Path,
) -> None:
    knowledge_file = tmp_path / "carrier-policy.md"
    knowledge_file.write_text(
        "# Carrier Policy\n\n"
        "Overview text.\n\n"
        "## Date Requirements\n\n"
        "Use YYYY-MM-DD.\n\n"
        "## Human Review\n\n"
        "Escalate unknown fields.",
        encoding="utf-8",
    )

    chunks = chunk_markdown_file(knowledge_file)

    assert len(chunks) == 3
    assert chunks[0].chunk_id == "carrier-policy-001"
    assert chunks[0].source_file == "carrier-policy.md"
    assert chunks[1].section == "Date Requirements"
    assert chunks[1].content == "Use YYYY-MM-DD."
    assert chunks[2].section == "Human Review"


def test_chunk_markdown_file_returns_empty_list_for_empty_file(
    tmp_path: Path,
) -> None:
    knowledge_file = tmp_path / "empty.md"
    knowledge_file.write_text("", encoding="utf-8")

    assert chunk_markdown_file(knowledge_file) == []