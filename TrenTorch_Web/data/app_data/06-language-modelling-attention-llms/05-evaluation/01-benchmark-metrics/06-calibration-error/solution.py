import numpy as np


def expected_calibration_error(confidences, correct, n_bins=10):
    conf = np.asarray(confidences, dtype=float)
    corr = np.asarray(correct, dtype=float)
    bins = np.clip(np.ceil(conf * n_bins).astype(int) - 1, 0, n_bins - 1)
    n = len(conf)
    ece = 0.0
    for b in range(n_bins):
        sel = bins == b
        if sel.any():
            ece += sel.sum() / n * abs(corr[sel].mean() - conf[sel].mean())
    return float(ece)


def brier_score(probs, outcomes):
    p = np.asarray(probs, dtype=float)
    y = np.asarray(outcomes, dtype=float)
    return float(((p - y) ** 2).mean())
