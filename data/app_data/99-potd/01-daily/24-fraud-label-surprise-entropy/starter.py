import numpy as np


def entropy(p: np.ndarray) -> float:
    """
    Shannon entropy, in bits.

    p: shape (k,), a probability distribution (sums to 1, within 1e-6).

    Return H(p) = -sum(p_i * log2(p_i)).

    p_i == 0 contributes exactly 0 to the sum (the standard convention,
    from the limit p*log(p) -> 0), not NaN: do not call log2 on a zero
    entry at all.
    """
    # TODO: mask out the zero-probability entries before taking log2.
    pass
