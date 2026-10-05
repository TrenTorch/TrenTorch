import numpy as np


def topic_conditional(
    doc_counts: np.ndarray,
    topic_word: np.ndarray,
    topic_totals: np.ndarray,
    alpha: float,
    beta: float,
    word: int,
) -> np.ndarray:
    doc_counts = np.asarray(doc_counts, dtype=float)
    topic_word = np.asarray(topic_word, dtype=float)
    topic_totals = np.asarray(topic_totals, dtype=float)
    if topic_word.ndim != 2:
        raise ValueError("topic_word must be (K, V)")
    K, V = topic_word.shape
    if doc_counts.shape != (K,) or topic_totals.shape != (K,):
        raise ValueError("doc_counts and topic_totals must have length K")
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive")
    if np.any(doc_counts < 0) or np.any(topic_word < 0) or np.any(topic_totals < 0):
        raise ValueError("counts must be nonnegative")
    if not (0 <= word < V):
        raise ValueError("word index out of range")
    weights = (doc_counts + alpha) * (topic_word[:, word] + beta) / (topic_totals + V * beta)
    return weights / weights.sum()
