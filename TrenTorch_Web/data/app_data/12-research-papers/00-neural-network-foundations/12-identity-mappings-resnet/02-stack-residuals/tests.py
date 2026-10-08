"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/12-identity-mappings-resnet/02-stack-residuals/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-residual-stack")
stack_residuals = _module.stack_residuals


import numpy as np


def test_1_empty_stack_returns_the_input():
    x = np.array([1.0, 2.0])
    np.testing.assert_allclose(stack_residuals(x, []), x)


def test_2_zero_blocks_leave_input_unchanged():
    x = np.array([3.0])
    np.testing.assert_allclose(stack_residuals(x, [lambda v: v * 0.0] * 5), x)


def test_3_blocks_compose_in_order():
    x = np.array([1.0])
    fs = [lambda v: v, lambda v: v * 2]
    # first: 1 + 1 = 2; then: 2 + 2*2 = 6
    np.testing.assert_allclose(stack_residuals(x, fs), [6.0])


def test_4_repeated_scaled_identity_compounds():
    x = np.array([1.0])
    out = stack_residuals(x, [lambda v: 0.1 * v] * 3)
    np.testing.assert_allclose(out, [1.1**3])


def test_5_keeps_shape_through_the_stack():
    out = stack_residuals(np.ones((2, 2)), [lambda v: v * 0.0] * 4)
    assert out.shape == (2, 2)


def test_6_does_not_mutate_the_input():
    x = np.array([1.0])
    stack_residuals(x, [lambda v: v])
    np.testing.assert_array_equal(x, [1.0])

