import numpy as np


def apply_rope(x: np.ndarray, position, base: float = 10000.0) -> np.ndarray:
    """
    x: shape (d,) for a single vector, or (seq_len, d) for a batch.
    position: a single int (matching a 1D x) or a list/array of ints,
    one per row (matching a 2D x). d must be even.

    Returns a same-shape array with each consecutive pair rotated.
    """
    # TODO: Compute theta_i = base**(-2i/d) once, multiply by position to
    # get each pair's rotation angle, then rotate x's even/odd halves.
    # See Theory for the exact rotation formula.
    pass
