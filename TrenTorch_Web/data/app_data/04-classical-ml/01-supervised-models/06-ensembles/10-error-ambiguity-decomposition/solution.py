import numpy as np


def ambiguity_decomposition(predictions: np.ndarray, target: np.ndarray) -> tuple:
    preds = np.asarray(predictions, dtype=float)
    y = np.asarray(target, dtype=float)
    ensemble = preds.mean(axis=0)
    ensemble_error = float(np.mean((ensemble - y) ** 2))
    individual_error = float(np.mean((preds - y) ** 2))
    ambiguity = float(np.mean((preds - ensemble) ** 2))
    return ensemble_error, individual_error, ambiguity
