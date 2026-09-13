import numpy as np


def alignment_tax(base_model_scores: np.ndarray, aligned_model_scores: np.ndarray) -> float:
    base_model_scores = np.asarray(base_model_scores, dtype=float)
    aligned_model_scores = np.asarray(aligned_model_scores, dtype=float)
    return float(np.mean(base_model_scores - aligned_model_scores))


def per_benchmark_regression(base_model_scores: np.ndarray, aligned_model_scores: np.ndarray) -> np.ndarray:
    return np.asarray(base_model_scores, dtype=float) - np.asarray(aligned_model_scores, dtype=float)


def has_net_alignment_tax(base_model_scores: np.ndarray, aligned_model_scores: np.ndarray) -> bool:
    return alignment_tax(base_model_scores, aligned_model_scores) > 0.0
