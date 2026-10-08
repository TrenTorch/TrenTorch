import numpy as np


def kernel_ridge_predict(K_train, y, K_test, lam):
    """
    K_train: kernel between training points, shape (n, n)
    y: training targets, shape (n,)
    K_test: kernel between test and training points, shape (m, n)
    lam: ridge regularization strength

    Returns:
        Predictions for the test points, shape (m,).
    """
    # TODO: Solve (K + lam I) alpha = y, then return K_test alpha (see Theory).
    pass
