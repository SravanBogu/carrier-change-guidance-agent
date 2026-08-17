from pathlib import Path

from carrier_guidance.retrieval_models import KnowledgeChunk


def chunk_markdown_file(path: Path) -> list[KnowledgeChunk]:
    text = path.read_text(encoding="utf-8").strip()

    if not text:
        return []

    title = path.stem.replace("-", " ").title()
    sections = _split_by_headings(text)

    chunks: list[KnowledgeChunk] = []

    for chunk_index, (section, content) in enumerate(sections, start=1):
        cleaned_content = content.strip()

        if not cleaned_content:
            continue

        chunks.append(
            KnowledgeChunk(
                chunk_id=f"{path.stem}-{chunk_index:03d}",
                title=title,
                content=cleaned_content,
                source_file=path.name,
                section=section,
                chunk_index=chunk_index,
            )
        )

    return chunks


def _split_by_headings(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading = "Introduction"
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("#"):
            if current_lines:
                sections.append(
                    (
                        current_heading,
                        "\n".join(current_lines).strip(),
                    )
                )
                current_lines = []

            current_heading = line.lstrip("#").strip()
            continue

        current_lines.append(line)

    if current_lines:
        sections.append(
            (
                current_heading,
                "\n".join(current_lines).strip(),
            )
        )

    return sections