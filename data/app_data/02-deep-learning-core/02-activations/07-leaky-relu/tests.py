"""
pytest data/app_data/02-deep-learning-core/02-activations/07-leaky-relu/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
leaky_relu_forward, leaky_relu_backward = _module.leaky_relu_forward, _module.leaky_relu_backward


def test_forward_positive_inputs_pass_through_unchanged():
    x = np.array([0.5, 1.0, 3.0])
    assert np.allclose(leaky_relu_forward(x), x)


def test_forward_negative_inputs_scaled_by_default_slope():
    x = np.array([-1.0, -2.0, -3.0])
    assert np.allclose(leaky_relu_forward(x), x * 0.01)


def test_forward_at_zero_is_zero():
    assert np.isclose(leaky_relu_forward(np.array([0.0]))[0], 0.0)


def test_forward_respects_custom_negative_slope():
    x = np.array([-2.0])
    assert np.isclose(leaky_relu_forward(x, negative_slope=0.2)[0], -0.4)


def test_forward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.leaky_relu
    x = np.array([-3.0, -1.0, 0.0, 0.5, 1.0, 3.0])
    expected = np.array([-0.03, -0.01, 0.0, 0.5, 1.0, 3.0])
    assert np.allclose(leaky_relu_forward(x), expected, atol=1e-8)


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.leaky_relu + autograd
    x = np.array([-3.0, -1.0, 0.0, 0.5, 1.0, 3.0])
    expected = np.array([0.01, 0.01, 0.01, 1.0, 1.0, 1.0])
    grad_output = np.ones_like(x)
    assert np.allclose(leaky_relu_backward(grad_output, x), expected, atol=1e-8)


def test_backward_negative_side_never_fully_zeroes_the_gradient():
    # The whole point of LeakyReLU over ReLU: negative-input units keep
    # a nonzero gradient (fixes the "dying ReLU" problem).
    x = np.array([-5.0])
    grad_output = np.array([1.0])
    result = leaky_relu_backward(grad_output, x)[0]
    assert result != 0.0
    assert np.isclose(result, 0.01)


def test_backward_respects_custom_negative_slope():
    x = np.array([-2.0])
    grad_output = np.array([1.0])
    assert np.isclose(leaky_relu_backward(grad_output, x, negative_slope=0.2)[0], 0.2)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    grad_output = rng.normal(size=10)
    analytic = leaky_relu_backward(grad_output, x)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        if abs(x[i]) < 1e-3:
            continue  # skip near the kink, finite differences are unreliable there
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (
            (leaky_relu_forward(x_plus)[i] - leaky_relu_forward(x_minus)[i])
            / (2 * eps)
            * grad_output[i]
        )
        assert np.isclose(analytic[i], numeric[i], atol=1e-4)


def test_backward_uses_negative_slope_not_zero_for_negative_inputs():
    # Directly targets a mutant that copy-pastes plain ReLU's backward
    # (grad_output * (x > 0)), silently dropping the negative_slope term
    # and reintroducing the dying-ReLU problem this activation exists to fix.
    x = np.array([-10.0])
    grad_output = np.array([1.0])
    result = leaky_relu_backward(grad_output, x)[0]
    assert not np.isclose(result, 0.0)
