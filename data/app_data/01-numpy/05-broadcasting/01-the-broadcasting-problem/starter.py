import numpy as np


def add_row_with_loop(matrix: np.ndarray, row: np.ndarray) -> np.ndarray:
    """
    Given a 2D array `matrix` and a 1D array `row` whose length
    matches matrix's number of columns, return a new array where
    `row` has been added to every row of `matrix`.

    Implement this using an explicit Python for loop over the
    rows of matrix (do not rely on broadcasting here — this
    function exists to contrast with the next one).
    """
    pass


def add_row_with_broadcasting(matrix: np.ndarray, row: np.ndarray) -> np.ndarray:
    """
    Given the same inputs as add_row_with_loop, produce the
    identical result using a single vectorized expression that
    relies on NumPy's broadcasting (matrix + row), with no
    explicit loop.
    """
    pass
