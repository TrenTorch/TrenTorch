import numpy as np


def marginal_x(joint: np.ndarray) -> np.ndarray:
    """
    `joint` is a 2D array where joint[i, j] = P(X=i, Y=j). The marginal
    distribution of X alone, P(X=i), sums out every value of Y:

        P(X=i) = sum_j(P(X=i, Y=j))
    """
    pass


def marginal_y(joint: np.ndarray) -> np.ndarray:
    """
    Same idea as marginal_x, summed the other way: P(Y=j) sums out
    every value of X.
    """
    pass


def conditional_x_given_y(joint: np.ndarray, y_index: int) -> np.ndarray:
    """
    P(X | Y=y_index): restrict to the single column where Y=y_index,
    then renormalize so it sums to 1 on its own (a valid probability
    distribution over X, not just an unnormalized slice of `joint`).
    """
    pass
