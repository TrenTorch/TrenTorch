"""
pytest data/app_data/02-deep-learning-core/02-activations/03-tanh/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
tanh_forward, tanh_backward = _module.tanh_forward, _module.tanh_backward


def test_forward_at_zero_is_zero():
    assert np.isclose(tanh_forward(np.array([0.0]))[0], 0.0)


def test_forward_stays_in_negative_one_one_range():
    x = np.array([-1000.0, -10.0, 0.0, 10.0, 1000.0])
    result = tanh_forward(x)
    assert np.all(result >= -1.0) and np.all(result <= 1.0)
    assert np.all(np.isfinite(result))


def test_forward_is_odd_function():
    # tanh(-x) == -tanh(x), the zero-centered symmetry sigmoid lacks.
    x = np.array([0.3, 1.5, 4.0])
    assert np.allclose(tanh_forward(-x), -tanh_forward(x))


def test_backward_matches_hand_computation():
    # at output=0.0, 1 - 0^2 = 1, so grad passes through unchanged
    output = np.array([0.0])
    grad_output = np.array([2.0])
    assert np.isclose(tanh_backward(grad_output, output)[0], 2.0)


def test_backward_matches_hand_computation_nonzero():
    # at output=0.5, 1 - 0.25 = 0.75
    output = np.array([0.5])
    grad_output = np.array([2.0])
    assert np.isclose(tanh_backward(grad_output, output)[0], 1.5)


def test_backward_is_maximal_at_output_zero():
    # 1 - y^2 peaks at y=0 (value 1.0) and shrinks toward +-1,
    # the same vanishing-gradient shape sigmoid's derivative has.
    grad_output = np.array([1.0])
    mid = tanh_backward(grad_output, np.array([0.0]))[0]
    near_neg_one = tanh_backward(grad_output, np.array([-0.99]))[0]
    near_pos_one = tanh_backward(grad_output, np.array([0.99]))[0]
    assert mid > near_neg_one
    assert mid > near_pos_one


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    grad_output = rng.normal(size=10)
    output = tanh_forward(x)
    analytic = tanh_backward(grad_output, output)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (
            (tanh_forward(x_plus)[i] - tanh_forward(x_minus)[i]) / (2 * eps) * grad_output[i]
        )
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_uses_one_minus_output_squared_not_something_else():
    # Directly targets a mutant that computes the derivative wrong,
    # e.g. (1 - output) instead of (1 - output**2): at output=0.5 the
    # correct factor is 0.75, a linear-instead-of-squared formula gives 0.5.
    grad_output = np.array([1.0])
    result = tanh_backward(grad_output, np.array([0.5]))
    assert np.isclose(result[0], 0.75)
