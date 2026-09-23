import numpy as np


def balanced_accuracy(labels: np.ndarray, predictions: np.ndarray) -> float:
    """
    The macro-average of per-class recall: compute recall separately
    within each class (what fraction of THAT class's samples were
    correctly predicted), then average those per-class recalls with
    equal weight, regardless of how many samples each class actually has.
    """
    # TODO: For each distinct class c, recall_c = mean(predictions == c
    # among samples where labels == c). Average those recalls across
    # classes (equal weight per class, not per sample).
    pass


def stratified_k_fold_split(
    labels: np.ndarray, k: int, seed: int | None = None
) -> list[tuple[np.ndarray, np.ndarray]]:
    """
    Like 01-splitting-and-resampling's k_fold_split, except each fold
    preserves the overall class proportions (a plain k_fold_split can,
    by bad luck, put very few or zero minority-class samples in some fold).

    Returns:
        k (train_idx, val_idx) pairs, same contract as k_fold_split.
    """
    # TODO: For EACH class separately: shuffle that class's own indices,
    # split them into k folds (np.array_split). Then for fold i,
    # val_idx is fold i from every class concatenated together, and
    # train_idx is every OTHER fold from every class concatenated.
    pass
