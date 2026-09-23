import numpy as np


def gaussian_elimination_solve(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Solves the square linear system a @ x = b via Gaussian elimination
    WITH PARTIAL PIVOTING -- no np.linalg.inv/solve/pinv anywhere in
    here, this function IS the solver those hide.

    At each column, swap in the row (at or below the current one) with
    the largest-magnitude entry in that column before eliminating, then
    back-substitute once the matrix is upper-triangular.

    a: shape (n, n), guaranteed invertible.
    b: shape (n,).
    Returns x, shape (n,), solving a @ x == b.
    """
    pass


def ridge_regression_predict(
    input: np.ndarray, target: np.ndarray, lam: float, queries: np.ndarray
) -> np.ndarray:
    """
    Fits ridge regression via the closed-form normal equation, solved
    with your own gaussian_elimination_solve above (never
    np.linalg.inv/solve/pinv), then predicts for every row of `queries`.

    Convention (deliberately different from `Ridge Regression (L2)`):
    the bias column is appended as the LAST column of the augmented
    design matrix, and regularization applies to every dimension of the
    normal equation, including the bias -- no zeroing the last
    diagonal entry.

    input: shape (n, d) training features.
    target: shape (n,) training targets.
    lam: non-negative L2 regularization strength.
    queries: shape (m, d) feature rows to predict for.
    Returns predictions, shape (m,).
    """
    pass
