
import numpy as np

from _load import load_solution

entropy = load_solution("math-entropy").entropy
cross_entropy = load_solution("math-cross-entropy").cross_entropy


def kl_divergence(p: np.ndarray, q: np.ndarray, base: float = 2.0) -> float:
    return cross_entropy(p, q, base) - entropy(p, base)
