import numpy as np


def ordinal_encode(values: np.ndarray, order: list) -> np.ndarray:
    rank = {label: i for i, label in enumerate(order)}
    return np.array([rank.get(v, -1) for v in values], dtype=int)


def target_encode(categories: np.ndarray, y: np.ndarray, smoothing: float = 0.0) -> dict:
    categories = np.asarray(categories)
    y = np.asarray(y, dtype=float)
    global_mean = y.mean()
    mapping = {}
    for category in np.unique(categories):
        rows = y[categories == category]
        n = len(rows)
        mapping[category] = float((n * rows.mean() + smoothing * global_mean) / (n + smoothing))
    return mapping


def apply_target_encoding(categories: np.ndarray, mapping: dict, default: float) -> np.ndarray:
    return np.array([mapping.get(c, default) for c in categories], dtype=float)


def out_of_fold_target_encode(
    categories: np.ndarray, y: np.ndarray, n_folds: int, smoothing: float = 0.0
) -> np.ndarray:
    categories = np.asarray(categories)
    y = np.asarray(y, dtype=float)
    encoded = np.empty(len(y))
    for block in np.array_split(np.arange(len(y)), n_folds):
        held_out = np.zeros(len(y), dtype=bool)
        held_out[block] = True
        mapping = target_encode(categories[~held_out], y[~held_out], smoothing)
        encoded[block] = apply_target_encoding(categories[block], mapping, float(y[~held_out].mean()))
    return encoded
