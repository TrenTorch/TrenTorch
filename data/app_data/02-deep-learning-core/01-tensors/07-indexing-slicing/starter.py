import numpy as np


def basic_slice(a: np.ndarray, start: int, stop: int) -> np.ndarray:
    """a[start:stop] along the first axis."""
    pass


def boolean_mask(a: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """a[mask], mask a same-shape (or broadcastable) boolean array."""
    pass


def fancy_index(a: np.ndarray, indices: np.ndarray) -> np.ndarray:
    """a[indices], indices an integer array."""
    pass


def is_a_view_of(child: np.ndarray, parent: np.ndarray) -> bool:
    """
    Whether `child`'s underlying memory overlaps `parent`'s, i.e.
    whether `child` is a VIEW of `parent` rather than an independent copy.
    """
    # TODO: np.shares_memory.
    pass
