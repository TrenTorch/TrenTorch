import numpy as np


def kernel_ridge_predict(K_train, y, K_test, lam):
    n = K_train.shape[0]
    alpha = np.linalg.solve(K_train + lam * np.eye(n), y)
    return K_test @ alpha
