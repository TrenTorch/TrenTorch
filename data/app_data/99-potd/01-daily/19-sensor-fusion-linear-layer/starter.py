import numpy as np


def linear_forward(W: np.ndarray, b: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    A single linear layer: y = W x + b.

    W: shape (d_out, d_in), already shaped for a direct W @ x (no transpose).
    b: shape (d_out,).
    x: shape (d_in,).

    Return y, shape (d_out,). No activation is applied.
    """
    # TODO: W @ x is the matrix-vector product; b then broadcasts elementwise.
    pass
