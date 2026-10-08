"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/03-deep-forest/03-cascade-predict/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-deep-forest-cascade-predict")
cascade_predict = _module.cascade_predict


import numpy as np


def test_1_single_forest_takes_its_argmax():
    out = cascade_predict([np.array([[0.1, 0.9], [0.8, 0.2]])])
    np.testing.assert_array_equal(out, [1, 0])


def test_2_two_forests_are_averaged_before_argmax():
    a = np.array([[0.9, 0.1]])
    b = np.array([[0.2, 0.8]])
    np.testing.assert_array_equal(cascade_predict([a, b]), [0])


def test_3_ties_go_to_the_first_class():
    out = cascade_predict([np.array([[0.5, 0.5]])])
    np.testing.assert_array_equal(out, [0])


def test_4_returns_integer_class_indices():
    out = cascade_predict([np.eye(3)])
    assert out.dtype.kind == "i"


def test_5_one_prediction_per_sample():
    assert cascade_predict([np.ones((5, 2))]).shape == (5,)


def test_6_does_not_mutate_the_inputs():
    p = np.array([[0.2, 0.8]])
    cascade_predict([p])
    np.testing.assert_array_equal(p, [[0.2, 0.8]])

