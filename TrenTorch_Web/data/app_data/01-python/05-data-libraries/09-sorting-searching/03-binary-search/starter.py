import numpy as np


def insertion_points(sorted_a: np.ndarray, values: np.ndarray, side: str) -> np.ndarray:
    """Where each value would be inserted into `sorted_a` ("left" or "right" side)."""
    # TODO: Binary search for every value.
    pass


def count_between(sorted_a: np.ndarray, lo, hi) -> int:
    """How many elements x of `sorted_a` satisfy lo <= x <= hi (two searches, no scan)."""
    # TODO: Subtract two insertion points.
    pass


def bucketize(values: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """
    Bin index of each value for increasing `edges`: the number of edges that are
    <= the value (0 below the first edge, len(edges) at or above the last).
    """
    # TODO: Count the edges at or below each value.
    pass


def nearest_value(sorted_a: np.ndarray, targets: np.ndarray) -> np.ndarray:
    """For each target, the element of `sorted_a` closest to it (the smaller one on a tie)."""
    # TODO: Compare the two neighbours around the insertion point.
    pass


def is_present(sorted_a: np.ndarray, values: np.ndarray) -> np.ndarray:
    """Boolean array: is each value an element of `sorted_a`?"""
    # TODO: Check the element at the insertion point.
    pass
