"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/12-identity-mappings-resnet/01-residual-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-residual-forward")
residual_forward = _module.residual_forward


import numpy as np


def test_1_zero_residual_returns_the_input():
    x = np.array([1.0, 2.0])
    np.testing.assert_allclose(residual_forward(x, lambda v: np.zeros_like(v)), x)


def test_2_adds_the_residual_branch():
    x = np.array([1.0, 2.0])
    np.testing.assert_allclose(residual_forward(x, lambda v: 3 * v), [4.0, 8.0])


def test_3_preserves_shape():
    out = residual_forward(np.ones((2, 3)), lambda v: v * 0.0)
    assert out.shape == (2, 3)


def test_4_works_on_scalars():
    assert abs(residual_forward(2.0, lambda v: v * 0.5) - 3.0) < 1e-12


def test_5_does_not_mutate_the_input():
    x = np.array([1.0, 2.0])
    residual_forward(x, lambda v: v)
    np.testing.assert_array_equal(x, [1.0, 2.0])


def test_6_identity_shortcut_is_exact():
    x = np.array([5.0])
    assert residual_forward(x, lambda v: v * 0.0)[0] == 5.0

