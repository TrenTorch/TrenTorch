"""
pytest data/app_data/02-deep-learning-core/04-autograd/02-backward-multiplication/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}")
mul_backward = _module.mul_backward


def test_mul_backward_matches_hand_computation():
    # z = 3*4=12, grad_output=1 -> grad_a=b=4, grad_b=a=3
    grad_a, grad_b = mul_backward(1.0, 3.0, 4.0)
    assert grad_a == 4.0
    assert grad_b == 3.0


def test_mul_backward_scales_with_grad_output():
    grad_a, grad_b = mul_backward(2.0, 3.0, 4.0)
    assert grad_a == 8.0
    assert grad_b == 6.0


def test_mul_backward_matches_finite_difference_check():
    def f(a, b):
        return a * b

    a0, b0, grad_output = 2.5, -1.5, 3.0
    eps = 1e-6
    numeric_grad_a = (f(a0 + eps, b0) - f(a0 - eps, b0)) / (2 * eps) * grad_output
    numeric_grad_b = (f(a0, b0 + eps) - f(a0, b0 - eps)) / (2 * eps) * grad_output

    grad_a, grad_b = mul_backward(grad_output, a0, b0)
    assert np.isclose(grad_a, numeric_grad_a)
    assert np.isclose(grad_b, numeric_grad_b)


def test_mul_backward_with_zero_input():
    grad_a, grad_b = mul_backward(1.0, 0.0, 5.0)
    assert grad_a == 5.0
    assert grad_b == 0.0


def test_mul_backward_with_negative_inputs():
    grad_a, grad_b = mul_backward(1.0, -2.0, 3.0)
    assert grad_a == 3.0
    assert grad_b == -2.0


def test_mul_backward_does_not_use_the_same_inputs_own_value():
    # Directly targets a mutant that computes grad_a using `a` instead
    # of `b` (and vice versa), a plausible copy-paste mistake given how
    # similar the two lines look. Using distinct a and b values makes
    # this mistake clearly detectable.
    grad_a, grad_b = mul_backward(1.0, 10.0, 2.0)
    assert grad_a == 2.0  # must be b, not a
    assert grad_b == 10.0  # must be a, not b
    assert grad_a != 10.0
    assert grad_b != 2.0
