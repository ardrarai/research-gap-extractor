"""
Purpose:
- Centralize all refusal rules and refusal messages.
- Enforce strict boundaries on what the system will not do.
- Redirect invalid requests toward allowed operations.

Responsibilities:
- Detect disallowed user intents (summaries, conclusions, generic ideas).
- Return consistent, firm refusal responses.

Forbidden:
- Do NOT perform input validation.
- Do NOT produce research outputs.
- Do NOT soften refusals with apologies or speculative language.
"""


# contracts/refusal.py

from config.constants import REFUSAL_MESSAGES


def get_refusal_message(error_code: str) -> str:
    return REFUSAL_MESSAGES.get(
        error_code,
        "Request cannot be processed due to invalid input."
    )
