"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/11-mixup/01-mixup-inputs/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mixup-inputs")
mixup_inputs = _module.mixup_inputs


import numpy as np


def test_1_lam_one_keeps_the_original_batch():
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(mixup_inputs(x, np.array([1, 0]), 1.0), x)


def test_2_lam_zero_returns_the_permuted_batch():
    x = np.array([[1.0], [3.0]])
    np.testing.assert_allclose(mixup_inputs(x, np.array([1, 0]), 0.0), [[3.0], [1.0]])


def test_3_lam_half_averages_each_pair():
    x = np.array([[0.0], [4.0]])
    np.testing.assert_allclose(mixup_inputs(x, np.array([1, 0]), 0.5), [[2.0], [2.0]])


def test_4_identity_permutation_returns_the_input():
    x = np.array([[5.0, 6.0]])
    np.testing.assert_allclose(mixup_inputs(x, np.array([0]), 0.3), x)


def test_5_keeps_the_batch_shape():
    x = np.ones((4, 3, 2))
    assert mixup_inputs(x, np.array([3, 2, 1, 0]), 0.7).shape == (4, 3, 2)


def test_6_does_not_mutate_the_input():
    x = np.array([[1.0], [2.0]])
    mixup_inputs(x, np.array([1, 0]), 0.5)
    np.testing.assert_array_equal(x, [[1.0], [2.0]])

