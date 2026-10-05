"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/11-smote/03-oversample/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-smote-oversample")
smote_oversample = _module.smote_oversample


import numpy as np


def test_1_output_shape():
    X = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 0.0]])
    assert smote_oversample(X, 5, 2, np.random.default_rng(0)).shape == (5, 2)


def test_2_new_points_stay_inside_the_minority_bounding_box():
    X = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 0.0]])
    out = smote_oversample(X, 50, 2, np.random.default_rng(1))
    assert np.all(out >= X.min(axis=0) - 1e-12) and np.all(out <= X.max(axis=0) + 1e-12)


def test_3_zero_new_samples_gives_empty_array():
    X = np.array([[0.0], [1.0]])
    assert smote_oversample(X, 0, 1, np.random.default_rng(2)).shape == (0, 1)


def test_4_same_seed_gives_same_samples():
    X = np.array([[0.0], [3.0], [6.0]])
    a = smote_oversample(X, 4, 2, np.random.default_rng(9))
    b = smote_oversample(X, 4, 2, np.random.default_rng(9))
    np.testing.assert_allclose(a, b)


def test_5_two_points_produce_samples_on_their_segment():
    X = np.array([[0.0], [10.0]])
    out = smote_oversample(X, 20, 1, np.random.default_rng(3))
    assert np.all(out >= 0.0 - 1e-12) and np.all(out <= 10.0 + 1e-12)


def test_6_does_not_mutate_the_minority_samples():
    X = np.array([[0.0], [1.0], [2.0]])
    smote_oversample(X, 3, 1, np.random.default_rng(4))
    np.testing.assert_array_equal(X, [[0.0], [1.0], [2.0]])

