import numpy as np


def pairwise_distances(input: np.ndarray, queries: np.ndarray) -> np.ndarray:
    """
    input:   shape (n_samples, n_features)
    queries: shape (n_queries, n_features)

    Returns:
        shape (n_queries, n_samples): Euclidean distance from every
        query point to every training point.
    """
    # TODO: Broadcast queries against input (queries[:, None, :] minus
    # input[None, :, :] gives shape (n_queries, n_samples, n_features)),
    # square, sum over the last axis, then sqrt.
    pass


def knn_predict(input: np.ndarray, labels: np.ndarray, queries: np.ndarray, k: int) -> np.ndarray:
    """
    Returns:
        shape (n_queries,): the majority class among each query's k
        nearest training points (by Euclidean distance). Ties broken
        by the lower class label.
    """
    # TODO: pairwise_distances(), then for each query take the k
    # smallest distances (np.argsort, then the first k columns), look
    # up those neighbors' labels, and take the majority vote (same
    # np.unique + argmax pattern as random_forest_predict).
    pass
