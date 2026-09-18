"""
pytest data/app_data/02-deep-learning-core/02-activations/02-sigmoid/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
sigmoid_forward, sigmoid_backward = _module.sigmoid_forward, _module.sigmoid_backward


def test_forward_at_zero_is_one_half():
    assert np.isclose(sigmoid_forward(np.array([0.0]))[0], 0.5)


def test_forward_stays_in_zero_one_range():
    x = np.array([-1000.0, -10.0, 0.0, 10.0, 1000.0])
    result = sigmoid_forward(x)
    assert np.all(result >= 0.0) and np.all(result <= 1.0)
    assert np.all(np.isfinite(result))


def test_backward_matches_hand_computation():
    output = np.array([0.5])
    grad_output = np.array([2.0])
    # f'(x) at output=0.5 is 0.5*0.5=0.25, so grad = 2.0*0.25 = 0.5
    assert np.isclose(sigmoid_backward(grad_output, output)[0], 0.5)


def test_backward_is_maximal_at_output_one_half():
    # sigmoid's derivative y*(1-y) peaks at y=0.5 (value 0.25) and
    # shrinks toward the extremes -- the classic vanishing-gradient shape.
    grad_output = np.array([1.0])
    mid = sigmoid_backward(grad_output, np.array([0.5]))[0]
    near_zero = sigmoid_backward(grad_output, np.array([0.01]))[0]
    near_one = sigmoid_backward(grad_output, np.array([0.99]))[0]
    assert mid > near_zero
    assert mid > near_one


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    grad_output = rng.normal(size=10)
    output = sigmoid_forward(x)
    analytic = sigmoid_backward(grad_output, output)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (
            (sigmoid_forward(x_plus)[i] - sigmoid_forward(x_minus)[i]) / (2 * eps) * grad_output[i]
        )
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_uses_output_directly_not_output_times_one_minus_something_else():
    # Directly targets a mutant that computes the derivative wrong,
    # e.g. output * (1 + output) instead of output * (1 - output):
    # at output=0.5 the correct derivative factor is 0.25, a wrong
    # formula gives a clearly different number.
    grad_output = np.array([1.0])
    result = sigmoid_backward(grad_output, np.array([0.5]))
    assert np.isclose(result[0], 0.25)
