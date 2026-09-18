"""
pytest data/app_data/02-deep-learning-core/04-autograd/01-backward-addition/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/04-autograd/{Path(__file__).resolve().parent.name}")
add_backward = _module.add_backward


def test_add_backward_passes_upstream_gradient_unchanged():
    grad_a, grad_b = add_backward(1.0)
    assert grad_a == 1.0
    assert grad_b == 1.0


def test_add_backward_scales_with_grad_output():
    grad_a, grad_b = add_backward(5.0)
    assert grad_a == 5.0
    assert grad_b == 5.0


def test_add_backward_gives_both_inputs_the_same_gradient():
    grad_a, grad_b = add_backward(3.7)
    assert grad_a == grad_b


def test_add_backward_matches_finite_difference_check():
    def f(a, b):
        return a + b

    a0, b0, grad_output = 2.0, -3.0, 4.0
    eps = 1e-6
    numeric_grad_a = (f(a0 + eps, b0) - f(a0 - eps, b0)) / (2 * eps) * grad_output
    numeric_grad_b = (f(a0, b0 + eps) - f(a0, b0 - eps)) / (2 * eps) * grad_output

    grad_a, grad_b = add_backward(grad_output)
    assert np.isclose(grad_a, numeric_grad_a)
    assert np.isclose(grad_b, numeric_grad_b)


def test_add_backward_handles_negative_upstream_gradient():
    grad_a, grad_b = add_backward(-2.5)
    assert grad_a == -2.5
    assert grad_b == -2.5


def test_add_backward_does_not_scale_the_gradient_incorrectly():
    # Directly targets a mutant that returns half the gradient to each
    # input (e.g. assuming addition somehow "splits" credit), instead
    # of passing the full upstream gradient to both.
    grad_a, grad_b = add_backward(10.0)
    assert grad_a == 10.0
    assert grad_b == 10.0
    assert not np.isclose(grad_a, 5.0)
