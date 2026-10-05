import numpy as np


def mutual_information(a: np.ndarray, b: np.ndarray) -> float:
    """
    Empirical mutual information in bits between two discrete 1-D arrays.
    Raise ValueError if the inputs are not 1-D with the same length.
    """
    pass


def chow_liu_tree(X: np.ndarray) -> list[tuple[int, int]]:
    """
    Maximum spanning tree over the columns of X, weighted by mutual information.
    Return sorted (i, j) tuples with i < j. Raise ValueError if X is not 2-D.
    """
    pass
