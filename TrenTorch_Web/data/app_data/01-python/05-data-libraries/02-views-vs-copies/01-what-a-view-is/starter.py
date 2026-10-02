import numpy as np


def is_view_of(candidate: np.ndarray, source: np.ndarray) -> bool:
    """
    Return True if `candidate` shares its underlying data buffer
    with `source` (i.e. `candidate` is a view into `source`'s
    memory, or vice versa, or both derive from the same buffer),
    False if they own completely independent buffers.

    Hint: np.shares_memory(a, b) answers exactly this question.
    """
    pass
