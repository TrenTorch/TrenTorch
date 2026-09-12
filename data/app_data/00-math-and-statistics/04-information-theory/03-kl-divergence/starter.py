import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

entropy = load_solution("00-math-and-statistics/04-information-theory/01-entropy").entropy
cross_entropy = load_solution("00-math-and-statistics/04-information-theory/02-cross-entropy").cross_entropy


def kl_divergence(p: np.ndarray, q: np.ndarray, base: float = 2.0) -> float:
    """
    KL divergence measures exactly the GAP Gibbs' inequality guarantees
    is non-negative: how many EXTRA bits cross-entropy costs, beyond
    the true distribution's own entropy.

        KL(p || q) = H(p, q) - H(p)

    `entropy` and `cross_entropy` are already provided above, this is
    a one-line combination of them, not a new formula to derive.
    """
    pass
