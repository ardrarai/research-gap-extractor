# structuring/sectioner.py

from collections import defaultdict


def group_chunks_by_section(chunks: list) -> dict:
    """
    Group chunks by detected section.

    Input:
    [
        {
            "chunk_id": str,
            "paper_id": str,
            "page_number": int,
            "section": str,
            "text": str
        }
    ]

    Output:
    {
        "introduction": [chunk, chunk, ...],
        "methods": [...],
        "results": [...],
        "unknown": [...]
    }
    """

    grouped = defaultdict(list)

    for chunk in chunks:
        section = chunk.get("section", "unknown")
        grouped[section].append(chunk)

    return dict(grouped)
