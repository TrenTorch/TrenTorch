import numpy as np


def oof_predictions(model_fn, X: np.ndarray, y: np.ndarray, n_splits: int = 3) -> np.ndarray:
    """
    Out-of-fold predictions using contiguous blocks. model_fn(X_train, y_train,
    X_test) returns predictions for X_test. Raises ValueError when n_splits is
    outside 2..n.
    """
    pass


def stacking_weights(P: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Least-squares weights (no intercept) combining the columns of P to fit y.
    Raises ValueError when P and y have different numbers of rows.
    """
    pass
