import numpy as np


def class_weights(y: np.ndarray) -> dict:
    y = np.asarray(y)
    labels, counts = np.unique(y, return_counts=True)
    n, k = len(y), len(labels)
    return {label.item(): float(n / (k * count)) for label, count in zip(labels, counts)}


def random_oversample(X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> tuple:
    X = np.asarray(X)
    y = np.asarray(y)
    labels, counts = np.unique(y, return_counts=True)
    largest = counts.max()
    extra = []
    for label, count in zip(labels, counts):
        if count < largest:
            rows = np.flatnonzero(y == label)
            extra.append(rng.choice(rows, size=largest - count, replace=True))
    picked = np.concatenate([np.arange(len(y))] + extra)
    return X[picked], y[picked]


def random_undersample(X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> tuple:
    X = np.asarray(X)
    y = np.asarray(y)
    labels, counts = np.unique(y, return_counts=True)
    smallest = counts.min()
    kept = []
    for label in labels:
        rows = np.flatnonzero(y == label)
        kept.append(np.sort(rng.choice(rows, size=smallest, replace=False)))
    picked = np.concatenate(kept)
    return X[picked], y[picked]


def interpolate_minority(minority: np.ndarray, n_new: int, rng: np.random.Generator) -> np.ndarray:
    minority = np.asarray(minority, dtype=float)
    points = np.empty((n_new, minority.shape[1]))
    for i in range(n_new):
        a_index, b_index = rng.choice(len(minority), size=2, replace=False)
        u = rng.random()
        a, b = minority[a_index], minority[b_index]
        points[i] = a + u * (b - a)
    return points
