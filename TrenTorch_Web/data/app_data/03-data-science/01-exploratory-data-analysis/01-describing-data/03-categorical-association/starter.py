import numpy as np


def contingency_table(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    a, b: 1D arrays of hashable labels, same length

    Returns:
        An int 2D array: rows are the sorted unique labels of a, columns
        the sorted unique labels of b, and entry (i, j) counts the rows
        where a is the i-th label and b is the j-th.
    """
    # TODO: Count every (a, b) combination.
    pass


def expected_counts(table: np.ndarray) -> np.ndarray:
    """
    Returns a float array of the same shape as table with entry (i, j)
    equal to row_total_i * column_total_j / grand_total.
    """
    # TODO: Build the counts independence would predict.
    pass


def chi_square_statistic(table: np.ndarray) -> float:
    """
    Returns the sum over cells of (observed - expected) ** 2 / expected,
    skipping cells whose expected count is 0.
    """
    # TODO: Sum the scaled departures from independence.
    pass


def cramers_v(table: np.ndarray) -> float:
    """
    Returns sqrt(chi2 / (n * min(r - 1, c - 1))) for a table with r rows,
    c columns and grand total n. Returns 0.0 when min(r - 1, c - 1) is 0
    or n is 0.
    """
    # TODO: Rescale the statistic to the range 0 to 1.
    pass
