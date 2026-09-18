"""
pytest data/app_data/11-production-ml/03-monitoring-and-drift/02-concept-drift-sliding-window/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/03-monitoring-and-drift/{Path(__file__).resolve().parent.name}")
sliding_window_accuracy = _module.sliding_window_accuracy
detect_concept_drift = _module.detect_concept_drift
first_drift_window = _module.first_drift_window


def _stream(seed, n, flip_probability):
    rng = np.random.default_rng(seed)
    predictions = rng.integers(0, 2, n)
    labels = predictions.copy()
    flips = rng.random(n) < flip_probability
    labels[flips] = 1 - labels[flips]
    return predictions, labels


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_sliding_window_accuracy_matches_hand_computation():
    predictions = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    labels = np.array([1, 1, 1, 0, 0, 0, 0, 1])
    accuracies = sliding_window_accuracy(predictions, labels, window_size=4)
    assert accuracies == [0.75, 0.75]


def test_02_detects_a_genuine_accuracy_drop():
    stable_preds, stable_labels = _stream(0, 400, flip_probability=0.05)
    _, degraded_labels = _stream(1, 400, flip_probability=0.5)
    combined_preds = np.concatenate([stable_preds, stable_preds])
    combined_labels = np.concatenate([stable_labels, degraded_labels])
    accuracies = sliding_window_accuracy(combined_preds, combined_labels, window_size=100)
    assert detect_concept_drift(accuracies, baseline_accuracy=0.95, drop_threshold=0.15)


# --- General-case coverage --------------------------------------------


def test_03_stable_accuracy_never_flags_drift():
    preds, labels = _stream(2, 500, flip_probability=0.02)
    accuracies = sliding_window_accuracy(preds, labels, window_size=100)
    assert not detect_concept_drift(accuracies, baseline_accuracy=0.95, drop_threshold=0.1)


def test_04_first_drift_window_finds_the_correct_index():
    accuracies = [0.95, 0.94, 0.5, 0.4]
    assert first_drift_window(accuracies, baseline_accuracy=0.95, drop_threshold=0.2) == 2


def test_05_first_drift_window_is_none_when_no_drift_occurs():
    accuracies = [0.95, 0.93, 0.94]
    assert first_drift_window(accuracies, baseline_accuracy=0.95, drop_threshold=0.2) is None


# --- Parameter handling -------------------------------------------------


def test_06_window_count_matches_expected_number_of_full_windows():
    predictions = np.zeros(105)
    labels = np.zeros(105)
    accuracies = sliding_window_accuracy(predictions, labels, window_size=10)
    assert len(accuracies) == 10  # 105 // 10, dropping the partial last window


def test_07_perfect_predictions_give_accuracy_of_one_everywhere():
    predictions = np.ones(40)
    labels = np.ones(40)
    accuracies = sliding_window_accuracy(predictions, labels, window_size=10)
    assert all(a == 1.0 for a in accuracies)


# --- Edge cases ---------------------------------------------------------


def test_08_drop_threshold_boundary_is_exclusive():
    assert not detect_concept_drift([0.8], baseline_accuracy=0.9, drop_threshold=0.1)


def test_09_all_wrong_predictions_give_zero_accuracy():
    predictions = np.zeros(10)
    labels = np.ones(10)
    accuracies = sliding_window_accuracy(predictions, labels, window_size=10)
    assert accuracies == [0.0]


# --- Independent correctness oracle -----------------------------------


def test_10_detect_concept_drift_checks_every_window_not_just_the_last():
    # Directly targets a mutant that only checks the FINAL window
    # (e.g. window_accuracies[-1]) instead of scanning all of them --
    # a drift that occurred and then RECOVERED must still be detected.
    accuracies = [0.95, 0.2, 0.94, 0.93]  # dip in the middle, recovers after
    assert detect_concept_drift(accuracies, baseline_accuracy=0.95, drop_threshold=0.3)
    assert first_drift_window(accuracies, baseline_accuracy=0.95, drop_threshold=0.3) == 1
