# evaluation/baseline.py

def simple_baseline_question(signal: dict) -> str:
    """
    Generate a simple heuristic question
    directly from signal excerpt.
    """

    text = signal.get("text_excerpt", "")
    signal_type = signal.get("signal_type", "")

    words = text.split()[:15]
    snippet = " ".join(words)

    if signal_type == "limitation":
        return f"What limitation exists regarding: {snippet}?"

    elif signal_type == "uncertainty":
        return f"What remains unclear about: {snippet}?"

    elif signal_type == "assumption":
        return f"What assumption is being made about: {snippet}?"

    else:
        return f"What research gap exists in: {snippet}?"
