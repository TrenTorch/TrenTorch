"""
pytest data/app_data/02-deep-learning-core/02-activations/06-swish/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
swish_forward, swish_backward = _module.swish_forward, _module.swish_backward


def test_forward_at_zero_is_zero():
    assert np.isclose(swish_forward(np.array([0.0]))[0], 0.0)


def test_forward_at_large_positive_x_approaches_identity():
    x = np.array([20.0])
    assert np.isclose(swish_forward(x)[0], 20.0, atol=1e-4)


def test_forward_at_large_negative_x_approaches_zero():
    x = np.array([-20.0])
    assert np.isclose(swish_forward(x)[0], 0.0, atol=1e-4)


def test_forward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.silu
    x = np.array([-3.0, -1.0, -0.5, 0.5, 1.0, 3.0])
    expected = np.array(
        [-0.14227762, -0.26894142, -0.18877033, 0.31122967, 0.73105858, 2.85772238]
    )
    assert np.allclose(swish_forward(x), expected, atol=1e-6)


def test_forward_dips_below_zero_for_small_negative_x():
    # The non-monotonic quirk that separates Swish from ReLU: Swish is
    # slightly negative around x = -1.28.
    x = np.array([-1.28])
    assert swish_forward(x)[0] < 0.0


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.silu + autograd
    x = np.array([-3.0, -1.0, -0.5, 0.5, 1.0, 3.0])
    expected = np.array(
        [-0.08810411, 0.07232949, 0.26003881, 0.73996119, 0.92767051, 1.08810411]
    )
    grad_output = np.ones_like(x)
    assert np.allclose(swish_backward(grad_output, x), expected, atol=1e-6)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    grad_output = rng.normal(size=10)
    analytic = swish_backward(grad_output, x)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (
            (swish_forward(x_plus)[i] - swish_forward(x_minus)[i]) / (2 * eps) * grad_output[i]
        )
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_includes_the_x_times_s_times_one_minus_s_term():
    # Directly targets a mutant that drops the second product-rule term
    # and returns just sigmoid(x) (as if Swish were plain sigmoid). At
    # x=2.0, sigmoid(x)~0.8808, but the correct full derivative is ~1.0904.
    x = np.array([2.0])
    grad_output = np.array([1.0])
    result = swish_backward(grad_output, x)[0]
    assert not np.isclose(result, 0.8808, atol=0.01)
    assert np.isclose(result, 1.09078431, atol=1e-6)
