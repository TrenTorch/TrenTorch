import numpy as np


def sorted_copy(a: np.ndarray) -> np.ndarray:
    """Return a sorted (ascending) copy of `a`; `a` is not changed."""
    # TODO: Sort without modifying the input.
    pass


def sort_order(a: np.ndarray) -> np.ndarray:
    """Indices that sort `a` ascending; ties keep their original order (stable)."""
    # TODO: A stable argsort.
    pass


def rank_of(a: np.ndarray) -> np.ndarray:
    """
    0-based rank of every element: the position it takes in the stable
    ascending order. rank_of([30, 10, 20]) -> [2, 0, 1].
    """
    # TODO: Invert the sorting order.
    pass


def descending_order(a: np.ndarray) -> np.ndarray:
    """Indices that sort `a` from largest to smallest; ties keep their original order."""
    # TODO: Stable order, largest first.
    pass


def sort_rows_by_column(m: np.ndarray, column: int) -> np.ndarray:
    """Rows of 2D `m` reordered by the values in `column` (ascending, stable)."""
    # TODO: Reorder whole rows by one column.
    pass
