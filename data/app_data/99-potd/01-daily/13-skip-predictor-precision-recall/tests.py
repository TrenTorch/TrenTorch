"""
pytest data/app_data/99-potd/01-daily/13-skip-predictor-precision-recall/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
precision_recall_f1 = _module.precision_recall_f1

TOLERANCE = 1e-6


def test_example_matches_the_specs_worked_counts():
    p = np.array([1, 1, 0, 1, 0, 0, 1, 0])
    y = np.array([1, 0, 0, 1, 0, 1, 1, 0])
    precision, recall, f1 = precision_recall_f1(p, y)
    assert abs(precision - 0.75) < TOLERANCE
    assert abs(recall - 0.75) < TOLERANCE
    assert abs(f1 - 0.75) < TOLERANCE


def test_no_predicted_positives_reports_zero_precision():
    p = np.zeros(10, dtype=int)
    y = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    precision, recall, f1 = precision_recall_f1(p, y)
    assert precision == 0.0
    assert recall == 0.0  # no TP at all either
    assert f1 == 0.0


def test_no_actual_positives_reports_zero_recall():
    p = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    y = np.zeros(10, dtype=int)
    precision, recall, f1 = precision_recall_f1(p, y)
    assert precision == 0.0  # every predicted positive is a false positive
    assert recall == 0.0
    assert f1 == 0.0


def test_perfect_predictions_give_all_ones():
    y = np.array([1, 0, 1, 1, 0, 0, 1, 0])
    p = y.copy()
    precision, recall, f1 = precision_recall_f1(p, y)
    assert abs(precision - 1.0) < TOLERANCE
    assert abs(recall - 1.0) < TOLERANCE
    assert abs(f1 - 1.0) < TOLERANCE


def test_matches_a_reference_on_random_batches():
    rng = np.random.default_rng(5)
    for _ in range(30):
        n = rng.integers(5, 500)
        p = rng.integers(0, 2, size=n)
        y = rng.integers(0, 2, size=n)
        tp = int(np.sum((p == 1) & (y == 1)))
        fp = int(np.sum((p == 1) & (y == 0)))
        fn = int(np.sum((p == 0) & (y == 1)))
        exp_precision = 0.0 if (tp + fp) == 0 else tp / (tp + fp)
        exp_recall = 0.0 if (tp + fn) == 0 else tp / (tp + fn)
        exp_f1 = (
            0.0
            if (exp_precision + exp_recall) == 0
            else 2 * exp_precision * exp_recall / (exp_precision + exp_recall)
        )
        precision, recall, f1 = precision_recall_f1(p, y)
        assert abs(precision - exp_precision) < TOLERANCE
        assert abs(recall - exp_recall) < TOLERANCE
        assert abs(f1 - exp_f1) < TOLERANCE


def test_large_n_within_the_time_budget():
    import time

    rng = np.random.default_rng(6)
    p = rng.integers(0, 2, size=1_000_000)
    y = rng.integers(0, 2, size=1_000_000)
    start = time.perf_counter()
    precision_recall_f1(p, y)
    elapsed = time.perf_counter() - start
    assert elapsed < 4.0, f"took {elapsed:.2f}s on n=1000000"
