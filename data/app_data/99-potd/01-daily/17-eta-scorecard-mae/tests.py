"""
pytest data/app_data/99-potd/01-daily/17-eta-scorecard-mae/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
mae = _module.mae

TOLERANCE = 1e-6


def test_example_matches_the_specs_worked_value():
    y = np.array([10.0, 15.0, 20.0, 12.0])
    yhat = np.array([12.0, 14.0, 18.0, 13.0])
    assert abs(mae(y, yhat) - 1.5) < TOLERANCE


def test_errors_in_both_directions_are_handled_the_same():
    y = np.array([10.0, 10.0])
    yhat_over = np.array([12.0, 12.0])
    yhat_under = np.array([8.0, 8.0])
    assert abs(mae(y, yhat_over) - 2.0) < TOLERANCE
    assert abs(mae(y, yhat_under) - 2.0) < TOLERANCE


def test_all_zero_error_gives_zero_mae():
    y = np.array([1.0, 2.0, 3.0])
    assert mae(y, y.copy()) == 0.0


def test_matches_a_reference_on_random_batches():
    rng = np.random.default_rng(12)
    for _ in range(20):
        n = rng.integers(1, 1000)
        y = rng.uniform(-1000, 1000, size=n)
        yhat = rng.uniform(-1000, 1000, size=n)
        expected = float(np.mean(np.abs(y - yhat)))
        assert abs(mae(y, yhat) - expected) < TOLERANCE


def test_large_n_within_the_time_budget():
    import time

    rng = np.random.default_rng(13)
    y = rng.uniform(-1000, 1000, size=1_000_000)
    yhat = rng.uniform(-1000, 1000, size=1_000_000)
    start = time.perf_counter()
    mae(y, yhat)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"took {elapsed:.2f}s on n=1000000"
