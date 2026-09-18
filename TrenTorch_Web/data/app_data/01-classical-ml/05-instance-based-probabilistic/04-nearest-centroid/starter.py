import numpy as np


def nearest_centroid_fit(input: np.ndarray, labels: np.ndarray) -> dict:
    """
    Returns a dict: {"classes": array (n_classes,), "centroids": array
    (n_classes, n_features)}, one centroid (the mean of that class's
    training rows) per class, in the same order as "classes".
    """
    # TODO: For each distinct class, average its rows of input.
    pass


def nearest_centroid_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    """
    Returns:
        shape (n_queries,): the class whose centroid is closest
        (Euclidean distance) to each query.
    """
    # TODO: Reuse 01-knn's pairwise_distances between the centroids and
    # queries, then for each query pick the class of the nearest one
    # (np.argmin along the centroid axis).
    pass
