# structuring/chunker.py

def chunk_pages(enriched_pages: list) -> list:
    """
    Convert page-level enriched data into reasoning chunks.

    v0 Strategy:
    - One page = one chunk
    - Preserve full traceability

    Input:
    [
        {
            "paper_id": str,
            "page_number": int,
            "section": str,
            "text": str
        }
    ]

    Output:
    [
        {
            "chunk_id": str,
            "paper_id": str,
            "page_number": int,
            "section": str,
            "text": str
        }
    ]
    """

    chunks = []

    for idx, page in enumerate(enriched_pages):
        if not page.get("text"):
            continue  # skip empty pages

        chunk = {
            "chunk_id": f"{page['paper_id']}_page_{page['page_number']}",
            "paper_id": page["paper_id"],
            "page_number": page["page_number"],
            "section": page["section"],
            "text": page["text"],
        }

        chunks.append(chunk)

    return chunks
