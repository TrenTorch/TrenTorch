import numpy as np


def sliding_window_accuracy(predictions: np.ndarray, labels: np.ndarray, window_size: int) -> list:
    predictions = np.asarray(predictions)
    labels = np.asarray(labels)
    correct = (predictions == labels).astype(float)
    n = len(correct)
    return [float(correct[i : i + window_size].mean()) for i in range(0, n - window_size + 1, window_size)]


def detect_concept_drift(window_accuracies: list, baseline_accuracy: float, drop_threshold: float) -> bool:
    return any(baseline_accuracy - accuracy > drop_threshold for accuracy in window_accuracies)


def first_drift_window(window_accuracies: list, baseline_accuracy: float, drop_threshold: float) -> int | None:
    for index, accuracy in enumerate(window_accuracies):
        if baseline_accuracy - accuracy > drop_threshold:
            return index
    return None
