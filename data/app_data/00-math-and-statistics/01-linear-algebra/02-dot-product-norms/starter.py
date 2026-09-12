import numpy as np


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    Mirrors np.dot(a, b) / torch.dot(a, b) for two 1D vectors:

        a . b = sum_i(a_i * b_i)

    A single scalar, the sum of the elementwise product.
    """
    pass


def l1_norm(x: np.ndarray) -> float:
    """
    The L1 ("Manhattan") norm: sum of absolute values.

        ||x||_1 = sum_i(|x_i|)
    """
    pass


def l2_norm(x: np.ndarray) -> float:
    """
    The L2 ("Euclidean") norm: the vector's straight-line length.

        ||x||_2 = sqrt(sum_i(x_i^2)) = sqrt(x . x)
    """
    pass


def linf_norm(x: np.ndarray) -> float:
    """
    The L-infinity ("max") norm: the single largest magnitude entry.

        ||x||_inf = max_i(|x_i|)
    """
    pass
