import numpy as np


def top_k(scores: np.ndarray, k: int) -> np.ndarray:
    order = np.argsort(-np.asarray(scores, dtype=float), kind="stable")
    return order[:k]


def competition_ranks(scores: np.ndarray) -> np.ndarray:
    scores = np.asarray(scores)
    ascending = np.sort(scores)
    return len(scores) - np.searchsorted(ascending, scores, side="right") + 1


def kth_largest(scores: np.ndarray, k: int):
    scores = np.asarray(scores)
    return np.partition(scores, len(scores) - k)[len(scores) - k]


def percentile_rank(scores: np.ndarray) -> np.ndarray:
    scores = np.asarray(scores)
    return np.searchsorted(np.sort(scores), scores, side="left") / len(scores)
