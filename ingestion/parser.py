# ingestion/parser.py

def clean_text(raw_text: str) -> str:
    """
    Perform minimal text cleanup.

    Philosophy:
    - Remove obvious noise
    - Preserve uncertainty, hedging, and weak language
    """

    if not raw_text:
        return ""

    # Normalize whitespace
    text = raw_text.replace("\n", " ")
    text = " ".join(text.split())

    return text
