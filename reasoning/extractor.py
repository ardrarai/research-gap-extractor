# reasoning/extractor.py

from reasoning.prompt_builder import build_unanswered_question_prompt
from reasoning.llm_client import call_ollama


def extract_unanswered_questions(signals: list, model: str = "phi3:mini") -> list:
    """
    Extract exactly one unanswered question per signal.
    """

    questions = []

    for idx, signal in enumerate(signals, start=1):
        prompt = build_unanswered_question_prompt(signal)
        response = call_ollama(prompt, model=model)

        if response.strip() == "NO_VALID_QUESTION":
            continue

        questions.append({
            "question_id": idx,
            "paper_id": signal["paper_id"],
            "page_number": signal["page_number"],
            "signal_type": signal["signal_type"],
            "content": response.strip()
        })

    return questions
