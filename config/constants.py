"""
Purpose:
- Centralise all hard constraints and non-negotiable rules of the system.
- Define limits that enforce research integrity and prevent misuse.
- Act as the policy layer that other modules must obey.

What belongs here:
- Minimum and maximum thresholds (e.g., number of papers, questions).
- Allowed and disallowed user intents.
- Fixed phrases used for refusals and warnings.
- Any constant that, if changed, alters the epistemic behaviour of the tool.

What does NOT belong here:
- Model-specific parameters (temperature, top-k, etc.).
- File paths or environment-specific values.
- Logic, functions, or conditional behaviour.
- Anything that is merely a preference rather than a rule.

Philosophy:
- If changing a value here makes the tool more permissive, less rigorous,
  or more hallucination-prone, it belongs in this file.
- This file exists to protect the user from misleading research outputs.
"""


# config/constants.py

"""
Policy-level constants that define non-negotiable research constraints.
"""

MIN_PAPERS = 3
MAX_QUESTIONS = 5

ALLOWED_EXTENSIONS = {".pdf", ".txt"}

REFUSAL_MESSAGES = {
    "TOO_FEW_PAPERS": "At least 3 papers are required to extract unresolved research questions.",
    "UNSUPPORTED_FILE": "Only PDF and text files are supported in v0.",
    "FILE_NOT_FOUND": "One or more provided paper paths do not exist.",
    "TOO_MANY_QUESTIONS": "Requested number of questions exceeds the allowed maximum.",
}
