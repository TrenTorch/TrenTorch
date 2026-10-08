"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/12-identity-mappings-resnet/03-identity-path-gradient/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-residual-gradient")
identity_path_gradient = _module.identity_path_gradient


import numpy as np


def test_1_zero_jacobian_passes_gradient_through():
    g = np.array([1.0, -2.0])
    np.testing.assert_allclose(identity_path_gradient(g, np.zeros((2, 2))), g)


def test_2_identity_jacobian_doubles_the_gradient():
    g = np.array([1.0, 2.0])
    np.testing.assert_allclose(identity_path_gradient(g, np.eye(2)), [2.0, 4.0])


def test_3_matches_the_chain_rule_for_a_linear_branch():
    g = np.array([1.0, 1.0])
    J = np.array([[0.5, 0.0], [0.0, -0.5]])
    np.testing.assert_allclose(identity_path_gradient(g, J), [1.5, 0.5])


def test_4_output_shape_matches_grad_out():
    assert identity_path_gradient(np.ones(3), np.zeros((3, 3))).shape == (3,)


def test_5_does_not_mutate_inputs():
    g = np.array([1.0, 2.0])
    identity_path_gradient(g, np.eye(2))
    np.testing.assert_array_equal(g, [1.0, 2.0])


def test_6_never_vanishes_when_the_branch_gradient_is_zero():
    g = np.array([0.7, -0.3])
    out = identity_path_gradient(g, np.zeros((2, 2)))
    assert np.all(out != 0)

