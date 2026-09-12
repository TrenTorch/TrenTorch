import numpy as np

_EPS = 1e-12


def cross_entropy(p: np.ndarray, q: np.ndarray, base: float = 2.0) -> float:
    """
    Cross-entropy between a TRUE distribution p and a PREDICTED
    distribution q:

        H(p, q) = -sum_i(p_i * log_base(q_i))

    Note this differs from 01-entropy's formula in exactly one place:
    the log is taken of q (the model's belief), while the outer
    multiplication is still by p (the true frequency). They're the
    same formula only when p == q.

    Clip q (not p) before taking the log, for the same log(0) reason
    01-entropy clips.
    """
    pass
