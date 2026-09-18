import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

pairwise_distances = load_solution(
    "01-classical-ml/05-instance-based-probabilistic/01-knn"
).pairwise_distances


def nearest_centroid_fit(input: np.ndarray, labels: np.ndarray) -> dict:
    classes = np.unique(labels)
    centroids = np.array([input[labels == c].mean(axis=0) for c in classes])
    return {"classes": classes, "centroids": centroids}


def nearest_centroid_predict(model: dict, queries: np.ndarray) -> np.ndarray:
    distances = pairwise_distances(model["centroids"], queries)
    nearest_class_idx = np.argmin(distances, axis=1)
    return model["classes"][nearest_class_idx]
