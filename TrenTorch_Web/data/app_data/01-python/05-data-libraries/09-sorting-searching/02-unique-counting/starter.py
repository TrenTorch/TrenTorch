import numpy as np


def distinct(a: np.ndarray) -> np.ndarray:
    """Sorted distinct values of `a`."""
    # TODO: Use np.unique.
    pass


def value_counts(a: np.ndarray):
    """(values, counts): the sorted distinct values and how often each occurs."""
    # TODO: Ask unique for the counts.
    pass


def first_positions(a: np.ndarray) -> np.ndarray:
    """For each sorted distinct value, the index of its first occurrence in `a`."""
    # TODO: Ask unique for the first indices.
    pass


def codes(a: np.ndarray) -> np.ndarray:
    """For each element, the index of its value among the sorted distinct values."""
    # TODO: Ask unique for the inverse.
    pass


def mode(a: np.ndarray):
    """The most frequent value; the smallest one if several tie."""
    # TODO: Pick the value with the largest count.
    pass


def unique_in_order(a: np.ndarray) -> np.ndarray:
    """Distinct values in the order they first appear in `a`."""
    # TODO: Sort the first positions, then read the array there.
    pass
