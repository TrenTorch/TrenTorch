"""
pytest data/app_data/99-potd/01-daily/22-lead-score-error-mse/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
mse = _module.mse

TOLERANCE = 1e-6


def test_example_matches_the_specs_worked_value():
    y = np.array([3.0, 5.0, 2.5, 7.0])
    yhat = np.array([2.5, 5.0, 4.0, 8.0])
    assert abs(mse(y, yhat) - 0.875) < TOLERANCE


def test_all_exact_predictions_give_zero_mse():
    y = np.array([1.0, 2.0, 3.0])
    assert mse(y, y.copy()) == 0.0


def test_squaring_happens_before_averaging_not_after():
    # Errors +2 and -2 would cancel if averaged before squaring (giving 0),
    # but must contribute 4 and 4 to the mean (giving 4), since each error
    # is squared first.
    y = np.array([10.0, 10.0])
    yhat = np.array([8.0, 12.0])
    assert abs(mse(y, yhat) - 4.0) < TOLERANCE


def test_a_single_outlier_dominates_the_average():
    y = np.array([0.0, 0.0, 0.0, 0.0])
    yhat = np.array([0.1, 0.1, 0.1, 100.0])
    # (0.01*3 + 10000) / 4, dominated by the one large error.
    expected = (0.1**2 * 3 + 100.0**2) / 4
    assert abs(mse(y, yhat) - expected) < 1e-3


def test_matches_a_reference_on_random_batches():
    rng = np.random.default_rng(20)
    for _ in range(20):
        n = rng.integers(1, 1000)
        y = rng.uniform(-1000, 1000, size=n)
        yhat = rng.uniform(-1000, 1000, size=n)
        expected = float(np.mean((y - yhat) ** 2))
        assert abs(mse(y, yhat) - expected) < 1e-3


def test_large_n_within_the_time_budget():
    import time

    rng = np.random.default_rng(21)
    y = rng.uniform(-1000, 1000, size=1_000_000)
    yhat = rng.uniform(-1000, 1000, size=1_000_000)
    start = time.perf_counter()
    mse(y, yhat)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"took {elapsed:.2f}s on n=1000000"
