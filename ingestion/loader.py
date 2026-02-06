# ingestion/loader.py

import pdfplumber
from pathlib import Path


def load_pdf(path: str) -> list:
    """
    Load a PDF and return a list of page-level raw text entries.

    Returns:
    [
        {
            "page_number": int,
            "text": str
        },
        ...
    ]
    """
    pages = []

    pdf_path = Path(path)

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({
                "page_number": i + 1,
                "text": text.strip()
            })

    return pages
