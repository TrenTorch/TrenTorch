"""
pytest data/app_data/02-deep-learning-core/02-activations/01-relu/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
relu_forward, relu_backward = _module.relu_forward, _module.relu_backward


def test_forward_matches_hand_computation():
    x = np.array([-2.0, -0.5, 0.0, 0.5, 2.0])
    assert np.array_equal(relu_forward(x), [0.0, 0.0, 0.0, 0.5, 2.0])


def test_backward_matches_hand_computation():
    x = np.array([-1.0, 2.0, -3.0, 4.0])
    grad_output = np.array([1.0, 1.0, 1.0, 1.0])
    result = relu_backward(grad_output, x)
    assert np.array_equal(result, [0.0, 1.0, 0.0, 1.0])


def test_backward_at_exactly_zero_is_zero():
    x = np.array([0.0])
    grad_output = np.array([1.0])
    assert relu_backward(grad_output, x)[0] == 0.0


def test_backward_scales_the_incoming_gradient():
    x = np.array([1.0, 1.0, -1.0])
    grad_output = np.array([5.0, -3.0, 5.0])
    result = relu_backward(grad_output, x)
    assert np.array_equal(result, [5.0, -3.0, 0.0])


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    x[np.abs(x) < 0.1] += 0.5  # avoid the non-differentiable point near 0
    grad_output = rng.normal(size=10)
    analytic = relu_backward(grad_output, x)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (relu_forward(x_plus)[i] - relu_forward(x_minus)[i]) / (2 * eps) * grad_output[i]
    assert np.allclose(analytic, numeric, atol=1e-4)
