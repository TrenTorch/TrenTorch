import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

precision_recall_f1 = load_solution(
    "01-classical-ml/07-evaluation/02-classification-metrics"
).precision_recall_f1


def f1_metric(labels: np.ndarray, predictions: np.ndarray) -> float:
    _, _, f1 = precision_recall_f1(labels, predictions)
    return f1


def optimize_threshold(
    labels: np.ndarray,
    scores: np.ndarray,
    metric_fn: Callable[[np.ndarray, np.ndarray], float] = f1_metric,
) -> tuple[float, float]:
    thresholds = np.unique(scores)

    best_threshold, best_score = float(thresholds[0]), float("-inf")
    for threshold in thresholds:
        predictions = (scores >= threshold).astype(int)
        score = metric_fn(labels, predictions)
        if score > best_score:
            best_score = score
            best_threshold = threshold

    return float(best_threshold), float(best_score)
