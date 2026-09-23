"""
pytest data/app_data/99-potd/01-daily/19-sensor-fusion-linear-layer/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
linear_forward = _module.linear_forward


def test_example_matches_the_specs_worked_values():
    W = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    b = np.array([0.5, -0.5])
    x = np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(linear_forward(W, b, x), [4.5, 4.5], atol=1e-6)


def test_d_out_equals_one_returns_a_length_one_array():
    W = np.array([[2.0, 3.0]])
    b = np.array([1.0])
    x = np.array([1.0, 1.0])
    y = linear_forward(W, b, x)
    assert y.shape == (1,)
    assert abs(y[0] - 6.0) < 1e-6


def test_large_negative_bias_is_not_clamped():
    W = np.array([[1.0]])
    b = np.array([-100.0])
    x = np.array([1.0])
    y = linear_forward(W, b, x)
    assert y[0] < 0


def test_a_non_square_transpose_bug_would_fail_this():
    # d_in != d_out: a wrongly-transposed W would raise a shape error here
    # instead of silently passing, unlike the square case.
    W = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])  # (2, 3): d_out=2, d_in=3
    b = np.zeros(2)
    x = np.array([1.0, 1.0, 1.0])
    y = linear_forward(W, b, x)
    np.testing.assert_allclose(y, [6.0, 15.0], atol=1e-6)


def test_matches_a_reference_on_random_shapes():
    rng = np.random.default_rng(14)
    for _ in range(20):
        d_in = rng.integers(1, 20)
        d_out = rng.integers(1, 20)
        W = rng.uniform(-5, 5, size=(d_out, d_in))
        b = rng.uniform(-5, 5, size=d_out)
        x = rng.uniform(-5, 5, size=d_in)
        expected = W @ x + b
        np.testing.assert_allclose(linear_forward(W, b, x), expected, atol=1e-6)


def test_max_size_within_the_time_budget():
    import time

    rng = np.random.default_rng(15)
    W = rng.uniform(-1, 1, size=(256, 256))
    b = rng.uniform(-1, 1, size=256)
    x = rng.uniform(-1, 1, size=256)
    start = time.perf_counter()
    linear_forward(W, b, x)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"took {elapsed:.2f}s at 256x256"
