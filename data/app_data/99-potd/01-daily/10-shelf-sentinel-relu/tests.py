"""
pytest data/app_data/99-potd/01-daily/10-shelf-sentinel-relu/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
relu_forward = _module.relu_forward


def test_example_matches_the_specs_worked_values():
    x = np.array([-2.0, 0.0, 3.0, -0.5, 1.5])
    g = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    activated, grad = relu_forward(x, g)
    np.testing.assert_allclose(activated, [0.0, 0.0, 3.0, 0.0, 1.5])
    np.testing.assert_allclose(grad, [0.0, 0.0, 1.0, 0.0, 1.0])


def test_exact_zero_input_gives_zero_gradient():
    x = np.array([0.0])
    g = np.array([5.0])
    activated, grad = relu_forward(x, g)
    assert activated[0] == 0.0
    assert grad[0] == 0.0


def test_all_negative_batch_is_entirely_zero():
    rng = np.random.default_rng(1)
    x = -rng.uniform(0.1, 100.0, size=50)
    g = rng.uniform(-10.0, 10.0, size=50)
    activated, grad = relu_forward(x, g)
    assert not activated.any()
    assert not grad.any()


def test_all_positive_batch_passes_the_gradient_through_unchanged():
    rng = np.random.default_rng(2)
    x = rng.uniform(0.1, 100.0, size=50)
    g = rng.uniform(-10.0, 10.0, size=50)
    activated, grad = relu_forward(x, g)
    np.testing.assert_allclose(activated, x)
    np.testing.assert_allclose(grad, g)


def test_matches_a_reference_on_random_mixed_batches():
    rng = np.random.default_rng(3)
    for _ in range(20):
        n = rng.integers(1, 200)
        x = rng.uniform(-50, 50, size=n)
        g = rng.uniform(-10, 10, size=n)
        activated, grad = relu_forward(x, g)
        np.testing.assert_allclose(activated, np.maximum(0, x))
        np.testing.assert_allclose(grad, g * (x > 0))


def test_large_batch_within_the_time_budget():
    import time

    rng = np.random.default_rng(4)
    x = rng.uniform(-100, 100, size=100_000)
    g = rng.uniform(-1, 1, size=100_000)
    start = time.perf_counter()
    activated, grad = relu_forward(x, g)
    elapsed = time.perf_counter() - start
    np.testing.assert_allclose(activated, np.maximum(0, x))
    np.testing.assert_allclose(grad, g * (x > 0))
    assert elapsed < 3.0, f"took {elapsed:.2f}s on n=100000"
