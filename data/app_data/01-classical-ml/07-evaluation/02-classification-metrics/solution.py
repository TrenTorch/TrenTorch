import numpy as np


def precision_recall_f1(labels: np.ndarray, predictions: np.ndarray) -> tuple[float, float, float]:
    true_positives = np.sum((predictions == 1) & (labels == 1))
    false_positives = np.sum((predictions == 1) & (labels == 0))
    false_negatives = np.sum((predictions == 0) & (labels == 1))

    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0.0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0.0
    )
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return float(precision), float(recall), float(f1)


def roc_curve(labels: np.ndarray, scores: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    thresholds = np.concatenate([[np.inf], np.sort(np.unique(scores))[::-1]])
    n_positive = np.sum(labels == 1)
    n_negative = np.sum(labels == 0)

    tpr_list, fpr_list = [], []
    for threshold in thresholds:
        predictions = (scores >= threshold).astype(int)
        true_positives = np.sum((predictions == 1) & (labels == 1))
        false_positives = np.sum((predictions == 1) & (labels == 0))
        tpr_list.append(true_positives / n_positive if n_positive > 0 else 0.0)
        fpr_list.append(false_positives / n_negative if n_negative > 0 else 0.0)

    return np.array(fpr_list), np.array(tpr_list), thresholds


def auc(fpr: np.ndarray, tpr: np.ndarray) -> float:
    order = np.argsort(fpr)
    return float(np.trapezoid(tpr[order], fpr[order]))
