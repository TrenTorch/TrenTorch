"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/11-smote/02-nearest-neighbors/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-smote-nearest")
nearest_neighbors = _module.nearest_neighbors


import numpy as np


def test_1_returns_k_indices():
    assert len(nearest_neighbors(np.arange(10.0).reshape(5, 2), np.zeros(2), 3)) == 3


def test_2_nearest_comes_first():
    X = np.array([[5.0], [1.0], [3.0]])
    np.testing.assert_array_equal(nearest_neighbors(X, np.array([0.0]), 3), [1, 2, 0])


def test_3_query_itself_is_the_closest_point():
    X = np.array([[0.0, 0.0], [4.0, 4.0]])
    assert nearest_neighbors(X, np.array([4.0, 4.0]), 1)[0] == 1


def test_4_k_one_returns_one_index():
    assert nearest_neighbors(np.array([[1.0], [2.0]]), np.array([0.0]), 1).tolist() == [0]


def test_5_returns_integer_indices():
    assert nearest_neighbors(np.ones((3, 2)), np.zeros(2), 2).dtype.kind == "i"


def test_6_does_not_mutate_inputs():
    X = np.array([[1.0], [2.0]])
    nearest_neighbors(X, np.array([0.0]), 1)
    np.testing.assert_array_equal(X, [[1.0], [2.0]])

