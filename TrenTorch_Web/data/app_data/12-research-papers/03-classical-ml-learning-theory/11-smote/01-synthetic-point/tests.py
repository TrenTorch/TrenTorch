"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/11-smote/01-synthetic-point/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-smote-point")
smote_point = _module.smote_point


import numpy as np


def test_1_u_zero_returns_the_sample():
    np.testing.assert_allclose(smote_point(np.array([1.0, 2.0]), np.array([3.0, 4.0]), 0.0), [1.0, 2.0])


def test_2_u_one_returns_the_neighbor():
    np.testing.assert_allclose(smote_point(np.array([1.0, 2.0]), np.array([3.0, 4.0]), 1.0), [3.0, 4.0])


def test_3_u_half_gives_the_midpoint():
    np.testing.assert_allclose(smote_point(np.array([0.0]), np.array([10.0]), 0.5), [5.0])


def test_4_result_lies_on_the_segment():
    x = np.array([1.0, 1.0])
    n = np.array([2.0, 5.0])
    p = smote_point(x, n, 0.3)
    assert np.all(p >= np.minimum(x, n) - 1e-12) and np.all(p <= np.maximum(x, n) + 1e-12)


def test_5_keeps_the_dimension():
    assert smote_point(np.ones(4), np.zeros(4), 0.2).shape == (4,)


def test_6_does_not_mutate_inputs():
    x = np.array([1.0])
    smote_point(x, np.array([2.0]), 0.5)
    np.testing.assert_array_equal(x, [1.0])

