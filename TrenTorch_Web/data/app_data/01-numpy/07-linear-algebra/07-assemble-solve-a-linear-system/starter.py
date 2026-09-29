import numpy as np


def solve_and_verify(coefficients: np.ndarray, constants: np.ndarray) -> dict:
    """
    `coefficients` is a square 2D array, `constants` is a 1D
    array of matching length.

    Perform the following, in order:
      1. Check whether `coefficients` is invertible (non-zero
         determinant, using a small tolerance). Call this
         `is_solvable`.
      2. If is_solvable is False, return immediately with:
         {"is_solvable": False, "solution": None, "residual_norm": None}
      3. If is_solvable is True, solve the system using
         np.linalg.solve to get `solution`.
      4. Compute the residual: coefficients @ solution - constants
         (this should be very close to a zero vector if the
         solve was correct).
      5. Compute residual_norm: the L2 norm of the residual
         vector, using np.linalg.norm.

    Return a dictionary:
      {
        "is_solvable": True,
        "solution": solution,
        "residual_norm": residual_norm
      }
    """
    pass
