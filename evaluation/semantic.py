# evaluation/semantic.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Load model once (small + fast)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Returns embeddings for list of texts.
    """
    return model.encode(texts, convert_to_numpy=True)


def semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Cosine similarity between two sentences.
    """
    emb = embed_texts([text_a, text_b])
    sim = cosine_similarity([emb[0]], [emb[1]])[0][0]
    return float(sim)


def best_semantic_match(pred: str, ground_truths: list) -> float:
    """
    Returns highest cosine similarity between prediction and any GT.
    """
    sims = [semantic_similarity(pred, gt) for gt in ground_truths]
    return max(sims) if sims else 0.0
