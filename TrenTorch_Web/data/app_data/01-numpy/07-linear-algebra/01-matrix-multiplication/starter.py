import numpy as np


def matmul_from_scratch(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute the matrix product of 2D arrays `a` (shape (m, n))
    and `b` (shape (n, p)), implementing the definition directly
    with explicit loops over i, j, and k — do NOT use @, matmul,
    or dot here. Return the resulting (m, p) array.
    This exists to build the definition into your understanding
    before using NumPy's built-in version below.
    """
    pass


def matmul_builtin(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute the same result as matmul_from_scratch, using the @
    operator.
    """
    pass


def compare_matmul_and_elementwise(a: np.ndarray, b: np.ndarray) -> dict:
    """
    Given two square matrices of the same shape, compute both
    a @ b and a * b.

    Return a dictionary:
      {
        "matmul_result": a @ b,
        "elementwise_result": a * b,
        "results_are_different": <True unless the two results
            happen to be identical, checked with array
            comparison, not assumed>
      }
    """
    pass
