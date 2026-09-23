import numpy as np


def ols_fit_predict(X: np.ndarray, y: np.ndarray, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Fit ordinary least squares by the normal equation and predict on Q.

    X: shape (n, d), training features. y: shape (n,), training targets.
    Q: shape (m, d), query features to predict on.

    Fold an intercept into X (and Q) as a leading column of ones, then solve
    w = pinv(X_aug) @ y using the Moore-Penrose pseudo-inverse, not a literal
    matrix inverse: production data can have collinear columns, which makes
    a hard inverse fail.

    Return (w, predictions): w has shape (d + 1,), intercept first;
    predictions has shape (m,), computed as Q_aug @ w.
    """
    # TODO: see Theory for why pinv rather than inv(X.T @ X) @ X.T.
    pass
