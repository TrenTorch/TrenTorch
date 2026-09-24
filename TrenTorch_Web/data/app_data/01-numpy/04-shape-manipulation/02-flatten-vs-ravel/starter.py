import numpy as np


def flatten_safe(arr: np.ndarray) -> np.ndarray:
    """
    Return a flattened (1D) version of `arr` that is guaranteed
    to be independent of `arr` — mutating the result must never
    affect `arr`. Use flatten(), not ravel().
    """
    pass


def flatten_efficient(arr: np.ndarray) -> np.ndarray:
    """
    Return a flattened (1D) version of `arr`, using ravel(),
    which may or may not share memory with `arr` depending on
    its layout.
    """
    pass


def compare_flatten_ravel(arr: np.ndarray) -> dict:
    """
    Given a multi-dimensional array `arr`:
      1. Compute f = arr.flatten()
      2. Compute r = arr.ravel()

    Return a dictionary:
      {
        "flatten_result": f,
        "ravel_result": r,
        "flatten_shares_memory": <bool, via np.shares_memory>,
        "ravel_shares_memory": <bool, via np.shares_memory>
      }
    """
    pass
