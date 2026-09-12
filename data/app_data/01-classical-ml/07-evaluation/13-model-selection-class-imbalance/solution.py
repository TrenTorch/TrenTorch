import numpy as np


def balanced_accuracy(labels: np.ndarray, predictions: np.ndarray) -> float:
    classes = np.unique(labels)
    per_class_recall = []
    for c in classes:
        mask = labels == c
        if mask.sum() > 0:
            per_class_recall.append(np.mean(predictions[mask] == c))
    return float(np.mean(per_class_recall))


def stratified_k_fold_split(
    labels: np.ndarray, k: int, seed: int | None = None
) -> list[tuple[np.ndarray, np.ndarray]]:
    rng = np.random.default_rng(seed)
    classes = np.unique(labels)

    per_class_folds = {}
    for c in classes:
        class_idx = rng.permutation(np.where(labels == c)[0])
        per_class_folds[c] = np.array_split(class_idx, k)

    splits = []
    for i in range(k):
        val_idx = np.concatenate([per_class_folds[c][i] for c in classes])
        train_idx = np.concatenate(
            [per_class_folds[c][j] for c in classes for j in range(k) if j != i]
        )
        splits.append((train_idx, val_idx))
    return splits
