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


def _match_patterns(text: str, patterns: List[str]) -> List[str]:
    """Return list of matched patterns (case-insensitive)."""
    matches = []
    lowered = text.lower()

    for pattern in patterns:
        if re.search(pattern, lowered):
            matches.append(pattern)

    return matches


def extract_signals(chunks: List[Dict]) -> List[Dict]:
    """
    Extract evidence signals from chunks.

    Input:
    [
        {
            "chunk_id": str,
            "paper_id": str,
            "page_number": int,
            "section": str,
            "text": str
        }
    ]

    Output:
    [
        {
            "signal_type": "limitation" | "uncertainty" | "assumption",
            "matched_patterns": [...],
            "paper_id": str,
            "page_number": int,
            "section": str,
            "text_excerpt": str
        }
    ]
    """

    signals = []

    for chunk in chunks:
        text = chunk.get("text", "")
        if not text:
            continue

        # --- limitation signals ---
        limitation_hits = _match_patterns(text, LIMITATION_PATTERNS)
        if limitation_hits:
            signals.append({
                "signal_type": "limitation",
                "matched_patterns": limitation_hits,
                "paper_id": chunk["paper_id"],
                "page_number": chunk["page_number"],
                "section": chunk["section"],
                "text_excerpt": text[:500]
            })

        # --- uncertainty signals ---
        uncertainty_hits = _match_patterns(text, UNCERTAINTY_PATTERNS)
        if uncertainty_hits:
            signals.append({
                "signal_type": "uncertainty",
                "matched_patterns": uncertainty_hits,
                "paper_id": chunk["paper_id"],
                "page_number": chunk["page_number"],
                "section": chunk["section"],
                "text_excerpt": text[:500]
            })

        # --- assumption signals ---
        assumption_hits = _match_patterns(text, ASSUMPTION_PATTERNS)
        if assumption_hits:
            signals.append({
                "signal_type": "assumption",
                "matched_patterns": assumption_hits,
                "paper_id": chunk["paper_id"],
                "page_number": chunk["page_number"],
                "section": chunk["section"],
                "text_excerpt": text[:500]
            })

    return signals
