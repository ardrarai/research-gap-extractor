# ingestion/metadata.py

SECTION_KEYWORDS = {
    "introduction": ["introduction", "background"],
    "methods": ["method", "materials", "methodology"],
    "results": ["result", "evaluation", "experiment"],
    "discussion": ["discussion"],
    "limitations": ["limitation", "future work", "constraints"],
    "conclusion": ["conclusion", "summary"]
}


def detect_section(text: str) -> str:
    """
    Heuristic section detection based on keyword presence.
    Returns a section label or 'unknown'.
    """

    lowered = text.lower()

    for section, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                return section

    return "unknown"


def attach_metadata(pages: list, paper_id: str) -> list:
    """
    Attach metadata to cleaned pages.

    Returns:
    [
        {
            "paper_id": "Paper A",
            "page_number": int,
            "section": str,
            "text": str
        }
    ]
    """
    enriched = []

    for page in pages:
        enriched.append({
            "paper_id": paper_id,
            "page_number": page["page_number"],
            "section": detect_section(page["text"]),
            "text": page["text"]
        })

    return enriched
