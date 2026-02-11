# evaluation/metrics.py

import re
from typing import List


def normalize_text(text: str) -> str:
    """
    Lowercase + remove non-alphanumeric characters + strip spaces.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()


def exact_match(pred: str, gt: str) -> int:
    """
    Returns 1 if normalized strings match exactly, else 0.
    """
    return int(normalize_text(pred) == normalize_text(gt))


def jaccard_similarity(pred: str, gt: str) -> float:
    """
    Computes Jaccard similarity between token sets.
    """
    pred_tokens = set(normalize_text(pred).split())
    gt_tokens = set(normalize_text(gt).split())

    if not pred_tokens or not gt_tokens:
        return 0.0

    intersection = pred_tokens.intersection(gt_tokens)
    union = pred_tokens.union(gt_tokens)

    return len(intersection) / len(union)


def precision_at_k(predictions: List[str], ground_truths: List[str], k: int) -> float:
    """
    Precision@k for a single paper.
    """
    if not predictions:
        return 0.0

    predictions = predictions[:k]

    matches = 0
    for pred in predictions:
        for gt in ground_truths:
            if exact_match(pred, gt):
                matches += 1
                break

    return matches / k
