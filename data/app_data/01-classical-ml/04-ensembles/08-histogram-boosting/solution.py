import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

information_gain = load_solution(
    "01-classical-ml/03-decision-trees/02-information-gain"
).information_gain


def build_histogram(values: np.ndarray, n_bins: int) -> np.ndarray:
    return np.linspace(values.min(), values.max(), n_bins + 1)


def find_best_split_histogram(
    input: np.ndarray, labels: np.ndarray, n_bins: int
) -> tuple[int, float, float] | None:
    n_features = input.shape[1]
    best_gain, best_feature, best_threshold = 0.0, None, None
    for feature in range(n_features):
        column = input[:, feature]
        edges = build_histogram(column, n_bins)
        candidate_thresholds = edges[1:-1]  # interior bin boundaries only
        for threshold in candidate_thresholds:
            left_mask = column <= threshold
            if left_mask.sum() == 0 or (~left_mask).sum() == 0:
                continue
            gain = information_gain(labels, labels[left_mask], labels[~left_mask])
            if gain > best_gain:
                best_gain, best_feature, best_threshold = gain, feature, threshold
    if best_feature is None:
        return None
    return best_feature, float(best_threshold), float(best_gain)
