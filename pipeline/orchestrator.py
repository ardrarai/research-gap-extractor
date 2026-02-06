# pipeline/orchestrator.py

from ingestion.loader import load_pdf
from ingestion.parser import clean_text
from ingestion.metadata import attach_metadata
from structuring.chunker import chunk_pages
from evidence.signals import extract_signals
from reasoning.extractor import extract_unanswered_questions


def run(validated_input: dict) -> str:
    papers = validated_input["papers"]
    max_questions = validated_input["max_questions"]

    all_questions = []

    for idx, paper_path in enumerate(papers):
        paper_id = f"Paper {chr(65 + idx)}"

        pages = load_pdf(paper_path)
        cleaned = [{**p, "text": clean_text(p["text"])} for p in pages]
        enriched = attach_metadata(cleaned, paper_id=paper_id)
        chunks = chunk_pages(enriched)

        signals = extract_signals(chunks)

        # 🔒 TEMP SAFETY CAP (ABSOLUTELY REQUIRED FOR CPU TESTING)
        signals = signals[:1]

        questions = extract_unanswered_questions(signals)
        all_questions.extend(questions)

    # Enforce max_questions
    all_questions = all_questions[:max_questions]

    if not all_questions:
        return "No strong unanswered questions detected from the provided papers."

    blocks = []
    for q in all_questions:
        block = f"""
{q['content']}

Source:
{q['paper_id']} — page {q['page_number']} ({q['signal_type']})
""".strip()
        blocks.append(block)

    return "\n\n".join(blocks)
