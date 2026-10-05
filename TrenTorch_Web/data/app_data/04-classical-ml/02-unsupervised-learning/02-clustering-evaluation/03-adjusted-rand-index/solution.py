import numpy as np


def _comb2(x):
    return x * (x - 1) / 2.0


def adjusted_rand_index(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    labels_true = np.asarray(labels_true)
    labels_pred = np.asarray(labels_pred)
    if labels_true.shape != labels_pred.shape:
        raise ValueError("labels must have the same length")
    n = labels_true.size
    _, true_idx = np.unique(labels_true, return_inverse=True)
    _, pred_idx = np.unique(labels_pred, return_inverse=True)
    table = np.zeros((true_idx.max() + 1, pred_idx.max() + 1))
    np.add.at(table, (true_idx, pred_idx), 1)
    sum_cells = np.sum(_comb2(table))
    sum_rows = np.sum(_comb2(table.sum(axis=1)))
    sum_cols = np.sum(_comb2(table.sum(axis=0)))
    total = _comb2(float(n))
    expected = sum_rows * sum_cols / total if total > 0 else 0.0
    max_index = (sum_rows + sum_cols) / 2.0
    denom = max_index - expected
    if denom == 0:
        return 1.0
    return float((sum_cells - expected) / denom)
