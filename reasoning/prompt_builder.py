# reasoning/prompt_builder.py

def build_unanswered_question_prompt(signal: dict) -> str:
    """
    Build a strict prompt that forces the LLM to derive
    exactly one unanswered research question from ONE evidence signal.
    """

    return f"""
You are a research assistant.

Your task:
- Derive exactly ONE unanswered research question.
- The question must arise ONLY from the provided evidence.
- The question must be specific and non-generic.
- Do NOT summarize the paper.
- Do NOT propose solutions.
- Do NOT invent new context.
- Do NOT discuss impact in broad or survey terms.

Evidence signal:
- Signal type: {signal['signal_type']}
- Paper: {signal['paper_id']}
- Page: {signal['page_number']}
- Section: {signal['section']}

Excerpt:
\"\"\"{signal['text_excerpt']}\"\"\"

Respond in the following strict format.
Do NOT add headings, markdown, or extra text.

QUESTION: <one clear, specific research question in a single sentence>
WHY: <one or two sentences explaining why this question exists based only on the evidence>
MISSING: <what data, experiment, comparison, or evaluation is missing>

If no valid unanswered research question can be derived from this evidence,
respond with exactly:
NO_VALID_QUESTION
""".strip()
