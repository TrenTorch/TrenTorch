import numpy as np


def get_independent_slice(arr: np.ndarray, start: int, stop: int) -> np.ndarray:
    """
    Return a slice of `arr` from `start` to `stop` that is fully
    independent of `arr` — mutating the returned array must never
    affect `arr`. Use slicing followed by .copy().
    """
    pass


def safe_modify_first_n(arr: np.ndarray, n: int, new_value) -> np.ndarray:
    """
    Return a NEW array based on `arr` where the first `n`
    elements are set to `new_value`, and the rest are unchanged
    from the original. Do not mutate `arr` itself in any way —
    use .copy() to obtain an independent array to modify.
    """
    pass
