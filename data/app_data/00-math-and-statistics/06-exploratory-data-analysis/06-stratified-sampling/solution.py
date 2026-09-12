import numpy as np


def class_proportions(labels: np.ndarray) -> dict:
    unique, counts = np.unique(labels, return_counts=True)
    return {label: count / len(labels) for label, count in zip(unique, counts)}


def stratified_sample_indices(labels: np.ndarray, sample_size: int, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    proportions = class_proportions(labels)

    selected = []
    for label, proportion in proportions.items():
        class_indices = np.where(labels == label)[0]
        n_from_class = round(proportion * sample_size)
        n_from_class = min(n_from_class, len(class_indices))
        chosen = rng.choice(class_indices, size=n_from_class, replace=False)
        selected.append(chosen)

    return np.concatenate(selected)
