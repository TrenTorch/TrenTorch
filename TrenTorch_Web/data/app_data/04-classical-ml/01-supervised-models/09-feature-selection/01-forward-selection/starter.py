import numpy as np


def forward_selection(X: np.ndarray, y: np.ndarray, k: int) -> list:
    """
    Greedily pick k columns of X, each step adding the column that maximizes
    the in-sample R^2 of an OLS fit with an intercept. Returns the indices in
    pick order. Raises ValueError if k is outside 1..d.
    """
    pass
