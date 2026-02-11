# pipeline/orchestrator.py

import json
import os

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

        # 🔒 TEMP SAFETY CAP (CPU-safe; remove later if needed)
        signals = signals[:1]

        questions = extract_unanswered_questions(signals)
        all_questions.extend(questions)

    # --- v1: rank questions by evidence strength ---
    all_questions.sort(
        key=lambda q: q.get("signal_score", 0),
        reverse=True
    )

    # Enforce max_questions AFTER ranking
    all_questions = all_questions[:max_questions]

    if not all_questions:
        return "No strong unanswered questions detected from the provided papers."

    # --- Save structured JSON output for evaluation ---
    os.makedirs("outputs", exist_ok=True)

    structured_output = []
    for q in all_questions:
        structured_output.append({
            "paper_id": q["paper_id"],
            "page_number": q["page_number"],
            "signal_type": q["signal_type"],
            "signal_score": q.get("signal_score", 0),
            "question": q["content"],
        })

    with open("outputs/latest_results.json", "w", encoding="utf-8") as f:
        json.dump(structured_output, f, indent=2)

    # --- Human-readable CLI output ---
    blocks = []
    for q in all_questions:
        block = f"""
{q['content']}

Source:
{q['paper_id']} — page {q['page_number']} ({q['signal_type']})
""".strip()
        blocks.append(block)

    return "\n\n".join(blocks)
