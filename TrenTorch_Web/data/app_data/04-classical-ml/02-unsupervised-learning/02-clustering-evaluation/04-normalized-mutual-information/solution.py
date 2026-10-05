import numpy as np


def normalized_mutual_information(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    labels_true = np.asarray(labels_true)
    labels_pred = np.asarray(labels_pred)
    if labels_true.shape != labels_pred.shape:
        raise ValueError("labels must have the same length")
    n = labels_true.size
    _, true_idx = np.unique(labels_true, return_inverse=True)
    _, pred_idx = np.unique(labels_pred, return_inverse=True)
    joint = np.zeros((true_idx.max() + 1, pred_idx.max() + 1))
    np.add.at(joint, (true_idx, pred_idx), 1)
    p_joint = joint / n
    p_true = p_joint.sum(axis=1)
    p_pred = p_joint.sum(axis=0)

    nonzero = p_joint > 0
    outer = np.outer(p_true, p_pred)
    mutual = np.sum(p_joint[nonzero] * np.log(p_joint[nonzero] / outer[nonzero]))
    h_true = -np.sum(p_true[p_true > 0] * np.log(p_true[p_true > 0]))
    h_pred = -np.sum(p_pred[p_pred > 0] * np.log(p_pred[p_pred > 0]))

    mean_entropy = (h_true + h_pred) / 2.0
    if mean_entropy == 0:
        return 1.0
    return float(max(mutual / mean_entropy, 0.0))
