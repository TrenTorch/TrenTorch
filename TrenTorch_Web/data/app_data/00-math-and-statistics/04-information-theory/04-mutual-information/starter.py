import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution

_cond_prob = load_solution("00-math-and-statistics/03-probability/04-conditional-probability")
marginal_x = _cond_prob.marginal_x
marginal_y = _cond_prob.marginal_y

kl_divergence = load_solution("00-math-and-statistics/04-information-theory/03-kl-divergence").kl_divergence


def mutual_information(joint: np.ndarray, base: float = 2.0) -> float:
    """
    Mutual information measures how far the actual joint distribution
    is from what it WOULD look like if X and Y were independent:

        MI(X; Y) = KL(P(X, Y) || P(X) * P(Y))

    Build the independent joint (the outer product of the two
    marginals, 03-probability/04-conditional-probability's own
    marginal_x/marginal_y are already provided above), then measure
    how far the real joint diverges from it, via KL divergence
    (already provided above too) on the two flattened tables.
    """
    pass
