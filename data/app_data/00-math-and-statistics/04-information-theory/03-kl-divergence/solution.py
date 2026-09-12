import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

entropy = load_solution("00-math-and-statistics/04-information-theory/01-entropy").entropy
cross_entropy = load_solution("00-math-and-statistics/04-information-theory/02-cross-entropy").cross_entropy


def kl_divergence(p: np.ndarray, q: np.ndarray, base: float = 2.0) -> float:
    return cross_entropy(p, q, base) - entropy(p, base)
