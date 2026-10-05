import numpy as np


def birch_subclusters(X: np.ndarray, threshold: float):
    X = np.asarray(X, dtype=float)
    if threshold < 0:
        raise ValueError("threshold must be nonnegative")
    counts = []
    linear = []
    squared = []
    labels = np.zeros(len(X), dtype=int)

    for i, x in enumerate(X):
        if counts:
            centroids = np.array([ls / n for ls, n in zip(linear, counts)])
            k = int(np.argmin(np.linalg.norm(centroids - x, axis=1)))
            n2 = counts[k] + 1
            ls2 = linear[k] + x
            ss2 = squared[k] + float(x @ x)
            radius_sq = ss2 / n2 - float((ls2 / n2) @ (ls2 / n2))
            radius = np.sqrt(max(radius_sq, 0.0))
            if radius <= threshold:
                counts[k] = n2
                linear[k] = ls2
                squared[k] = ss2
                labels[i] = k
                continue
        counts.append(1)
        linear.append(x.copy())
        squared.append(float(x @ x))
        labels[i] = len(counts) - 1

    centroids = np.array([ls / n for ls, n in zip(linear, counts)])
    return labels, centroids
