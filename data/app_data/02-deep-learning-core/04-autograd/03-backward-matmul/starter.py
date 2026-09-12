import numpy as np


def matmul_backward(grad_output: np.ndarray, a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    For C = A @ B (A is (m, k), B is (k, n), C is (m, n)), given
    grad_output (dL/dC, shape (m, n)), returns (dL/dA, dL/dB).

    A single matmul, `03-matrix-multiplication` (Math & Statistics)'s
    own operation, now needs a matrix-shaped generalization of
    Backward for multiplication's scalar rule, this is where shapes
    start to genuinely matter for a backward pass, not just values.
    """
    pass
