import numpy as np


def _weights(p_pdf, q_pdf, draws: np.ndarray) -> np.ndarray:
    draws = np.asarray(draws, dtype=float)
    return np.asarray(p_pdf(draws), dtype=float) / np.asarray(q_pdf(draws), dtype=float)


def importance_estimate(f, p_pdf, q_pdf, draws: np.ndarray) -> float:
    draws = np.asarray(draws, dtype=float)
    w = _weights(p_pdf, q_pdf, draws)
    return float(np.mean(np.asarray(f(draws), dtype=float) * w))


def self_normalized_estimate(f, p_pdf, q_pdf, draws: np.ndarray) -> float:
    draws = np.asarray(draws, dtype=float)
    w = _weights(p_pdf, q_pdf, draws)
    return float(np.sum(np.asarray(f(draws), dtype=float) * w) / np.sum(w))


def effective_sample_size(weights: np.ndarray) -> float:
    weights = np.asarray(weights, dtype=float)
    return float(weights.sum() ** 2 / np.sum(weights**2))
