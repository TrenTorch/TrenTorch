from itertools import combinations_with_replacement

import numpy as np


def polynomial_features_multivariate(X: np.ndarray, degree: int) -> np.ndarray:
    n, num_features = X.shape
    columns = []
    for d in range(degree + 1):
        for combo in combinations_with_replacement(range(num_features), d):
            column = np.ones(n)
            for feature_index in combo:
                column = column * X[:, feature_index]
            columns.append(column)
    return np.stack(columns, axis=1)
