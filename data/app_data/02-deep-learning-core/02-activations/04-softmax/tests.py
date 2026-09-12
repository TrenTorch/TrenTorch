"""
pytest data/app_data/02-deep-learning-core/02-activations/04-softmax/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
softmax_forward, softmax_backward = _module.softmax_forward, _module.softmax_backward


def test_forward_rows_sum_to_one():
    x = np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0]])
    result = softmax_forward(x)
    assert np.allclose(result.sum(axis=-1), 1.0)


def test_forward_uniform_input_gives_uniform_output():
    x = np.array([[5.0, 5.0, 5.0, 5.0]])
    result = softmax_forward(x)
    assert np.allclose(result, 0.25)


def test_forward_is_shift_invariant():
    # softmax(x) == softmax(x + c) for any constant c per row.
    x = np.array([[1.0, 2.0, 3.0]])
    assert np.allclose(softmax_forward(x), softmax_forward(x + 100.0))
    assert np.allclose(softmax_forward(x), softmax_forward(x - 100.0))


def test_forward_does_not_overflow_on_large_inputs():
    x = np.array([[1000.0, 1001.0, 999.0]])
    result = softmax_forward(x)
    assert np.all(np.isfinite(result))
    assert np.allclose(result.sum(axis=-1), 1.0)


def test_forward_largest_logit_gets_largest_probability():
    x = np.array([[1.0, 5.0, 2.0]])
    result = softmax_forward(x)
    assert np.argmax(result[0]) == 1


def test_backward_matches_hand_computation():
    # output = [0.5, 0.5], grad_output = [1.0, 0.0]
    # dot = 0.5*1.0 + 0.5*0.0 = 0.5
    # dL/dx_0 = 0.5 * (1.0 - 0.5) = 0.25
    # dL/dx_1 = 0.5 * (0.0 - 0.5) = -0.25
    output = np.array([[0.5, 0.5]])
    grad_output = np.array([[1.0, 0.0]])
    result = softmax_backward(grad_output, output)
    assert np.allclose(result, [[0.25, -0.25]])


def test_backward_sums_to_zero_per_row():
    # A structural property of softmax's Jacobian-vector product: since
    # every row of softmax's output sums to a constant (1), the gradient
    # w.r.t. any perturbation that shifts all inputs equally is zero, and
    # the per-row backward output always sums to zero.
    rng = np.random.default_rng(0)
    output = softmax_forward(rng.normal(size=(5, 4)))
    grad_output = rng.normal(size=(5, 4))
    result = softmax_backward(grad_output, output)
    assert np.allclose(result.sum(axis=-1), 0.0, atol=1e-10)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(3, 5))
    grad_output = rng.normal(size=(3, 5))
    output = softmax_forward(x)
    analytic = softmax_backward(grad_output, output)

    eps = 1e-5
    numeric = np.empty_like(x)
    for r in range(x.shape[0]):
        for c in range(x.shape[1]):
            x_plus, x_minus = x.copy(), x.copy()
            x_plus[r, c] += eps
            x_minus[r, c] -= eps
            f_plus = np.sum(softmax_forward(x_plus)[r] * grad_output[r])
            f_minus = np.sum(softmax_forward(x_minus)[r] * grad_output[r])
            numeric[r, c] = (f_plus - f_minus) / (2 * eps)
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_uses_the_dot_product_reduction_not_a_plain_elementwise_product():
    # Directly targets a mutant that treats softmax like an elementwise
    # activation, e.g. grad_output * output * (1 - output), instead of
    # the correct row-coupled formula output * (grad_output - dot).
    # With output=[0.2, 0.8] and grad_output=[1.0, 1.0]:
    #   correct: dot = 0.2+0.8 = 1.0, result = output*(1-1.0) = [0, 0]
    #   wrong (elementwise sigmoid-style): output*(1-output)*grad_output
    #     = [0.16, 0.16], clearly nonzero
    output = np.array([[0.2, 0.8]])
    grad_output = np.array([[1.0, 1.0]])
    result = softmax_backward(grad_output, output)
    assert np.allclose(result, [[0.0, 0.0]], atol=1e-10)
