"""
Purpose:
- Validate all user inputs before the pipeline executes.
- Enforce minimum paper count and supported file types.
- Reject unsupported user intents at the boundary.

Responsibilities:
- Check number of input papers (>= minimum).
- Verify file extensions and existence.
- Reject free-form or unsupported prompts.

Forbidden:
- Do NOT parse or read file contents.
- Do NOT attempt to correct invalid inputs.
- Do NOT contain any pipeline or LLM logic.
"""


# contracts/input_contract.py

from pathlib import Path
from config.constants import MIN_PAPERS, MAX_QUESTIONS, ALLOWED_EXTENSIONS


class InputValidationError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def validate_inputs(papers, max_questions):
    if len(papers) < MIN_PAPERS:
        raise InputValidationError("TOO_FEW_PAPERS")

    for p in papers:
        path = Path(p)
        if not path.exists():
            raise InputValidationError("FILE_NOT_FOUND")
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise InputValidationError("UNSUPPORTED_FILE")

    if max_questions > MAX_QUESTIONS:
        raise InputValidationError("TOO_MANY_QUESTIONS")

    return {
        "papers": papers,
        "max_questions": max_questions,
    }
