"""
pytest data/app_data/02-deep-learning-core/02-activations/08-mish/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
mish_forward, mish_backward = _module.mish_forward, _module.mish_backward


def test_forward_at_zero_is_zero():
    assert np.isclose(mish_forward(np.array([0.0]))[0], 0.0)


def test_forward_at_large_positive_x_approaches_identity():
    x = np.array([20.0])
    assert np.isclose(mish_forward(x)[0], 20.0, atol=1e-4)


def test_forward_at_large_negative_x_approaches_zero():
    x = np.array([-20.0])
    assert np.isclose(mish_forward(x)[0], 0.0, atol=1e-4)


def test_forward_does_not_overflow_on_large_inputs():
    x = np.array([1000.0, -1000.0])
    result = mish_forward(x)
    assert np.all(np.isfinite(result))


def test_forward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.mish
    x = np.array([-3.0, -1.0, -0.5, 0.5, 1.0, 3.0])
    expected = np.array(
        [-0.14564746, -0.30340146, -0.22074377, 0.37524521, 0.86509839, 2.98653500]
    )
    assert np.allclose(mish_forward(x), expected, atol=1e-6)


def test_forward_dips_below_zero_for_small_negative_x():
    x = np.array([-1.0])
    assert mish_forward(x)[0] < 0.0


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.mish + autograd
    x = np.array([-3.0, -1.0, -0.5, 0.5, 1.0, 3.0])
    expected = np.array(
        [-0.09339311, 0.05921676, 0.28951068, 0.88642438, 1.04903622, 1.02110691]
    )
    grad_output = np.ones_like(x)
    assert np.allclose(mish_backward(grad_output, x), expected, atol=1e-6)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    grad_output = rng.normal(size=10)
    analytic = mish_backward(grad_output, x)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (
            (mish_forward(x_plus)[i] - mish_forward(x_minus)[i]) / (2 * eps) * grad_output[i]
        )
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_uses_the_full_chained_derivative_not_plain_tanh_of_softplus():
    # Directly targets a mutant that drops the x * (1 - t^2) * sigmoid(x)
    # correction term and returns just t = tanh(softplus(x)) (as if Mish
    # behaved like plain tanh-of-something with no product-rule term).
    # At x=1.0 the correct derivative is ~1.04904, clearly different from
    # tanh(softplus(1.0)) ~0.86510.
    x = np.array([1.0])
    grad_output = np.array([1.0])
    result = mish_backward(grad_output, x)[0]
    assert not np.isclose(result, 0.86510, atol=0.01)
    assert np.isclose(result, 1.04903622, atol=1e-6)
