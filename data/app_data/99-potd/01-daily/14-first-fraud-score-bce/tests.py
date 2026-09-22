"""
pytest data/app_data/99-potd/01-daily/14-first-fraud-score-bce/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
bce_loss = _module.bce_loss

TOLERANCE = 1e-6


def test_example_matches_the_specs_worked_value():
    y = np.array([1.0, 0.0, 1.0, 0.0])
    yhat = np.array([0.9, 0.2, 0.6, 0.3])
    assert abs(bce_loss(y, yhat) - 0.299001) < 1e-5


def test_near_boundary_predictions_are_numerically_stable():
    y = np.array([1.0, 0.0])
    yhat = np.array([1 - 1e-7, 1e-7])
    loss = bce_loss(y, yhat)
    assert np.isfinite(loss)
    assert loss >= 0


def test_all_labels_the_same_class_only_uses_one_term():
    y = np.ones(5)
    yhat = np.array([0.9, 0.8, 0.95, 0.7, 0.85])
    expected = -np.mean(np.log(yhat))
    assert abs(bce_loss(y, yhat) - expected) < TOLERANCE


def test_perfect_predictions_give_a_loss_near_zero():
    y = np.array([1.0, 0.0, 1.0, 0.0])
    yhat = np.array([1 - 1e-7, 1e-7, 1 - 1e-7, 1e-7])
    assert bce_loss(y, yhat) < 1e-5


def test_matches_a_reference_on_random_batches():
    rng = np.random.default_rng(7)
    for _ in range(20):
        n = rng.integers(1, 1000)
        y = rng.integers(0, 2, size=n).astype(float)
        yhat = rng.uniform(1e-6, 1 - 1e-6, size=n)
        expected = -np.mean(y * np.log(yhat) + (1 - y) * np.log(1 - yhat))
        assert abs(bce_loss(y, yhat) - expected) < TOLERANCE


def test_large_n_within_the_time_budget():
    import time

    rng = np.random.default_rng(8)
    y = rng.integers(0, 2, size=100_000).astype(float)
    yhat = rng.uniform(1e-6, 1 - 1e-6, size=100_000)
    start = time.perf_counter()
    bce_loss(y, yhat)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"took {elapsed:.2f}s on n=100000"
