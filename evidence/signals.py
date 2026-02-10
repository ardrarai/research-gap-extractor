# evidence/signals.py

import re
from typing import List, Dict


# --- Signal phrase banks (intentionally conservative) ---

LIMITATION_PATTERNS = [
    r"limitation",
    r"limitations",
    r"future work",
    r"further research",
    r"not evaluated",
    r"not investigated",
    r"was not assessed",
    r"remains to be determined"
]

UNCERTAINTY_PATTERNS = [
    r"may ",
    r"might ",
    r"could ",
    r"suggests?",
    r"appears? to",
    r"unclear",
    r"unknown",
    r"not clear"
]

ASSUMPTION_PATTERNS = [
    r"we assume",
    r"it is assumed",
    r"is generally assumed",
    r"is widely accepted",
    r"commonly believed",
    r"it is believed"
]


# --- v1 signal strength weights ---
# Higher = more research-significant

SIGNAL_TYPE_WEIGHT = {
    "limitation": 3,
    "uncertainty": 2,
    "assumption": 1
}

SECTION_WEIGHT = {
    "methods": 3,
    "results": 3,
    "discussion": 2,
    "introduction": 1,
    "unknown": 1
}

# Minimum score required to keep a signal
MIN_SIGNAL_SCORE = 4


def _match_patterns(text: str, patterns: List[str]) -> List[str]:
    """Return list of matched patterns (case-insensitive)."""
    matches = []
    lowered = text.lower()

    for pattern in patterns:
        if re.search(pattern, lowered):
            matches.append(pattern)

    return matches


def _score_signal(
    signal_type: str,
    matched_patterns: List[str],
    section: str
) -> int:
    """
    Compute a conservative signal strength score.
    """

    score = 0

    # Base weight from signal type
    score += SIGNAL_TYPE_WEIGHT.get(signal_type, 0)

    # More matched patterns = stronger evidence
    score += len(matched_patterns)

    # Section importance
    score += SECTION_WEIGHT.get(section.lower(), SECTION_WEIGHT["unknown"])

    return score


def extract_signals(chunks: List[Dict]) -> List[Dict]:
    """
    Extract and score evidence signals from chunks.

    Only signals above MIN_SIGNAL_SCORE are retained.
    """

    signals = []

    for chunk in chunks:
        text = chunk.get("text", "")
        if not text:
            continue

        section = chunk.get("section", "unknown")

        # --- limitation signals ---
        limitation_hits = _match_patterns(text, LIMITATION_PATTERNS)
        if limitation_hits:
            score = _score_signal("limitation", limitation_hits, section)
            if score >= MIN_SIGNAL_SCORE:
                signals.append({
                    "signal_type": "limitation",
                    "matched_patterns": limitation_hits,
                    "signal_score": score,
                    "paper_id": chunk["paper_id"],
                    "page_number": chunk["page_number"],
                    "section": section,
                    "text_excerpt": text[:500]
                })

        # --- uncertainty signals ---
        uncertainty_hits = _match_patterns(text, UNCERTAINTY_PATTERNS)
        if uncertainty_hits:
            score = _score_signal("uncertainty", uncertainty_hits, section)
            if score >= MIN_SIGNAL_SCORE:
                signals.append({
                    "signal_type": "uncertainty",
                    "matched_patterns": uncertainty_hits,
                    "signal_score": score,
                    "paper_id": chunk["paper_id"],
                    "page_number": chunk["page_number"],
                    "section": section,
                    "text_excerpt": text[:500]
                })

        # --- assumption signals ---
        assumption_hits = _match_patterns(text, ASSUMPTION_PATTERNS)
        if assumption_hits:
            score = _score_signal("assumption", assumption_hits, section)
            if score >= MIN_SIGNAL_SCORE:
                signals.append({
                    "signal_type": "assumption",
                    "matched_patterns": assumption_hits,
                    "signal_score": score,
                    "paper_id": chunk["paper_id"],
                    "page_number": chunk["page_number"],
                    "section": section,
                    "text_excerpt": text[:500]
                })

    return signals
