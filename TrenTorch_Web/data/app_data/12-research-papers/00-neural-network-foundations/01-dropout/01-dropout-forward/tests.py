"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/01-dropout/01-dropout-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-dropout-forward")
dropout_forward = _module.dropout_forward


def test_1_kept_units_are_rescaled_by_one_over_one_minus_p():
    out = dropout_forward(np.array([1.0, 2.0]), np.array([1, 0]), p=0.5)
    np.testing.assert_allclose(out, [2.0, 0.0])


def test_2_dropped_units_become_zero():
    out = dropout_forward(np.array([3.0, 4.0, 5.0]), np.array([0, 0, 0]), p=0.3)
    np.testing.assert_array_equal(out, [0.0, 0.0, 0.0])


def test_3_no_dropout_leaves_values_unchanged():
    x = np.array([[1.0, -2.0], [0.5, 4.0]])
    np.testing.assert_allclose(dropout_forward(x, np.ones_like(x), p=0.0), x)


def test_4_works_on_matrices_with_the_same_shape():
    x = np.ones((2, 3))
    mask = np.array([[1, 0, 1], [0, 1, 0]])
    out = dropout_forward(x, mask, p=0.5)
    assert out.shape == (2, 3)
    np.testing.assert_allclose(out, mask * 2.0)


def test_5_does_not_mutate_input():
    x = np.array([1.0, 2.0])
    dropout_forward(x, np.array([1, 1]), p=0.5)
    np.testing.assert_array_equal(x, [1.0, 2.0])


def test_6_matches_a_hand_computed_case():
    # p=0.2 keeps the survivors at 1/0.8 = 1.25 times their value.
    out = dropout_forward(np.array([4.0, 8.0]), np.array([1, 1]), p=0.2)
    np.testing.assert_allclose(out, [5.0, 10.0])
