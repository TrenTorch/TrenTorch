import numpy as np


def pairwise_distances(input: np.ndarray, queries: np.ndarray) -> np.ndarray:
    diff = queries[:, np.newaxis, :] - input[np.newaxis, :, :]
    return np.sqrt(np.sum(diff**2, axis=-1))


def knn_predict(input: np.ndarray, labels: np.ndarray, queries: np.ndarray, k: int) -> np.ndarray:
    distances = pairwise_distances(input, queries)
    nearest_indices = np.argsort(distances, axis=1)[:, :k]

    predictions = np.empty(queries.shape[0], dtype=int)
    for i in range(queries.shape[0]):
        neighbor_labels = labels[nearest_indices[i]]
        values, counts = np.unique(neighbor_labels, return_counts=True)
        predictions[i] = values[np.argmax(counts)]
    return predictions
