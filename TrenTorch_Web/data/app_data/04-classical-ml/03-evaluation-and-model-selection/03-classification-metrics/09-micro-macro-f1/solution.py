import numpy as np


def _checked(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length")
    if y_true.size == 0:
        raise ValueError("inputs are empty")
    return y_true, y_pred


def _f1_from_counts(tp, fp, fn):
    denom = 2 * tp + fp + fn
    return 0.0 if denom == 0 else 2 * tp / denom


def f1_micro(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true, y_pred = _checked(y_true, y_pred)
    tp = fp = fn = 0
    for c in np.union1d(y_true, y_pred):
        actual = y_true == c
        predicted = y_pred == c
        tp += np.sum(actual & predicted)
        fp += np.sum(~actual & predicted)
        fn += np.sum(actual & ~predicted)
    return float(_f1_from_counts(tp, fp, fn))


def f1_macro(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true, y_pred = _checked(y_true, y_pred)
    scores = []
    for c in np.union1d(y_true, y_pred):
        actual = y_true == c
        predicted = y_pred == c
        tp = np.sum(actual & predicted)
        fp = np.sum(~actual & predicted)
        fn = np.sum(actual & ~predicted)
        scores.append(_f1_from_counts(tp, fp, fn))
    return float(np.mean(scores))
