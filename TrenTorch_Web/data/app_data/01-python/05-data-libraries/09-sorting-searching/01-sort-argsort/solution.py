import numpy as np


def sorted_copy(a: np.ndarray) -> np.ndarray:
    return np.sort(a)


def sort_order(a: np.ndarray) -> np.ndarray:
    return np.argsort(a, kind="stable")


def rank_of(a: np.ndarray) -> np.ndarray:
    order = np.argsort(a, kind="stable")
    ranks = np.empty_like(order)
    ranks[order] = np.arange(len(a))
    return ranks


def descending_order(a: np.ndarray) -> np.ndarray:
    return np.argsort(-np.asarray(a, dtype=float), kind="stable")


def sort_rows_by_column(m: np.ndarray, column: int) -> np.ndarray:
    return m[np.argsort(m[:, column], kind="stable")]
