"""
pytest data/app_data/99-potd/01-daily/21-brightness-dial-sigmoid/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
sigmoid_forward = _module.sigmoid_forward


def test_example_matches_the_specs_worked_value():
    sigma, grad = sigmoid_forward(np.array([0.5]))
    assert abs(sigma[0] - 0.622459) < 1e-5
    assert abs(grad[0] - 0.235004) < 1e-5


def test_zero_is_the_exact_midpoint():
    sigma, grad = sigmoid_forward(np.array([0.0]))
    assert abs(sigma[0] - 0.5) < 1e-12
    assert abs(grad[0] - 0.25) < 1e-12


def test_large_negative_x_does_not_overflow():
    sigma, grad = sigmoid_forward(np.array([-50.0]))
    assert np.isfinite(sigma[0])
    assert np.isfinite(grad[0])
    assert sigma[0] < 1e-10


def test_large_positive_x_does_not_overflow():
    sigma, grad = sigmoid_forward(np.array([50.0]))
    assert np.isfinite(sigma[0])
    assert np.isfinite(grad[0])
    assert sigma[0] > 1 - 1e-10


def test_matches_a_reference_on_random_values():
    rng = np.random.default_rng(18)
    x = rng.uniform(-50, 50, size=1000)
    sigma, grad = sigmoid_forward(x)
    expected_sigma = 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
    # Only compare where the naive reference itself doesn't overflow.
    safe = np.abs(x) < 30
    np.testing.assert_allclose(sigma[safe], expected_sigma[safe], atol=1e-6)
    np.testing.assert_allclose(grad, sigma * (1 - sigma), atol=1e-9)


def test_large_n_within_the_time_budget():
    import time

    rng = np.random.default_rng(19)
    x = rng.uniform(-50, 50, size=100_000)
    start = time.perf_counter()
    sigmoid_forward(x)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"took {elapsed:.2f}s on n=100000"
