"""
pytest data/app_data/99-potd/01-daily/29-cancellation-sanity-check-accuracy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
accuracy = _module.accuracy

TOLERANCE = 1e-6


def test_example_matches_the_specs_worked_value():
    p = np.array([1, 0, 1, 1, 0, 0])
    y = np.array([1, 0, 0, 1, 0, 1])
    assert abs(accuracy(p, y) - 0.666667) < 1e-5


def test_all_correct_gives_exactly_one():
    y = np.array([1, 0, 1, 0, 1])
    assert accuracy(y.copy(), y) == 1.0


def test_all_wrong_gives_exactly_zero():
    p = np.array([1, 0, 1, 0])
    y = np.array([0, 1, 0, 1])
    assert accuracy(p, y) == 0.0


def test_matches_a_reference_on_random_batches():
    rng = np.random.default_rng(27)
    for _ in range(20):
        n = rng.integers(1, 500)
        p = rng.integers(0, 2, size=n)
        y = rng.integers(0, 2, size=n)
        expected = float(np.mean(p == y))
        assert abs(accuracy(p, y) - expected) < TOLERANCE


def test_large_n_within_the_time_budget():
    import time

    rng = np.random.default_rng(28)
    p = rng.integers(0, 2, size=1_000_000)
    y = rng.integers(0, 2, size=1_000_000)
    start = time.perf_counter()
    accuracy(p, y)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"took {elapsed:.2f}s on n=1000000"
