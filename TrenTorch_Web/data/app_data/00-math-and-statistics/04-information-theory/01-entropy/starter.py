import numpy as np

_EPS = 1e-12


def entropy(probs: np.ndarray, base: float = 2.0) -> float:
    """
    Shannon entropy of a discrete probability distribution:

        H(P) = -sum_i(p_i * log_base(p_i))

    `base=2` gives entropy in bits (the standard unit, and the default
    here); `base=e` (np.e) gives entropy in nats.

    Clip probs before taking the log (to [_EPS, 1.0]) to avoid log(0):
    by convention, p * log(p) is treated as 0 when p = 0 (its limiting
    value), not as 0 * -inf = nan.
    """
    pass
