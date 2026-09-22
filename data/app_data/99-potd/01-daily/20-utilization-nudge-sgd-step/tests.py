"""
pytest data/app_data/99-potd/01-daily/20-utilization-nudge-sgd-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
sgd_step = _module.sgd_step


def test_example_matches_the_specs_worked_values():
    theta = np.array([1.0, 2.0])
    grad = np.array([0.2, -0.1])
    np.testing.assert_allclose(sgd_step(theta, grad, 0.1), [0.98, 2.01], atol=1e-6)


def test_eta_equals_one_subtracts_the_full_gradient():
    theta = np.array([5.0, -3.0])
    grad = np.array([1.5, -2.0])
    np.testing.assert_allclose(sgd_step(theta, grad, 1.0), theta - grad, atol=1e-6)


def test_zero_gradient_leaves_parameters_unchanged():
    theta = np.array([1.0, 2.0, 3.0])
    grad = np.zeros(3)
    np.testing.assert_allclose(sgd_step(theta, grad, 0.5), theta, atol=1e-12)


def test_matches_a_reference_on_random_vectors():
    rng = np.random.default_rng(16)
    for _ in range(20):
        d = rng.integers(1, 500)
        theta = rng.uniform(-10, 10, size=d)
        grad = rng.uniform(-10, 10, size=d)
        eta = rng.uniform(0.001, 1.0)
        expected = theta - eta * grad
        np.testing.assert_allclose(sgd_step(theta, grad, eta), expected, atol=1e-9)


def test_large_d_within_the_time_budget():
    import time

    rng = np.random.default_rng(17)
    theta = rng.uniform(-10, 10, size=10_000)
    grad = rng.uniform(-10, 10, size=10_000)
    start = time.perf_counter()
    sgd_step(theta, grad, 0.1)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"took {elapsed:.2f}s at d=10000"
