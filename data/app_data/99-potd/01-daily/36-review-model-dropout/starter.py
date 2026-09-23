import numpy as np


def inverted_dropout(x: np.ndarray, m: np.ndarray, p_keep: float) -> np.ndarray:
    """
    Inverted dropout, mask given directly.

    x: shape (n,), activations. m: shape (n,), 0/1 mask (given, not generated).
    p_keep: the keep probability used to generate m.

    Return (x * m) / p_keep. A dropped unit (m_i == 0) is 0.0 regardless of
    p_keep. p_keep == 1.0 is the identity.
    """
    # TODO: mask first (zeroes the dropped units), then scale the survivors.
    pass
