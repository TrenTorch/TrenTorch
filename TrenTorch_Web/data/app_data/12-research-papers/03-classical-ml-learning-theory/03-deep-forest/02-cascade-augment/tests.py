"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/03-deep-forest/02-cascade-augment/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-deep-forest-cascade-augment")
cascade_augment = _module.cascade_augment


import numpy as np


def test_1_output_has_features_plus_classes_columns():
    assert cascade_augment(np.ones((4, 3)), np.ones((4, 2))).shape == (4, 5)


def test_2_original_features_come_first():
    out = cascade_augment(np.array([[1.0, 2.0]]), np.array([[0.1, 0.9]]))
    np.testing.assert_allclose(out[:, :2], [[1.0, 2.0]])


def test_3_class_vectors_come_last():
    out = cascade_augment(np.array([[1.0]]), np.array([[0.2, 0.8]]))
    np.testing.assert_allclose(out[:, 1:], [[0.2, 0.8]])


def test_4_rows_are_preserved_in_order():
    X = np.arange(6.0).reshape(3, 2)
    out = cascade_augment(X, np.zeros((3, 1)))
    np.testing.assert_allclose(out[:, :2], X)


def test_5_works_with_one_class():
    assert cascade_augment(np.ones((2, 2)), np.zeros((2, 1))).shape == (2, 3)


def test_6_does_not_mutate_inputs():
    X = np.ones((2, 2))
    cascade_augment(X, np.zeros((2, 1)))
    np.testing.assert_array_equal(X, np.ones((2, 2)))

