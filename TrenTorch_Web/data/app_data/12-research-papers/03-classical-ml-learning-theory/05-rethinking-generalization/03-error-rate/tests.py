"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/05-rethinking-generalization/03-error-rate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-generalization-error-rate")
error_rate = _module.error_rate


import numpy as np


def test_1_all_correct_gives_zero():
    assert error_rate(np.array([0, 1, 2]), np.array([0, 1, 2])) == 0.0


def test_2_all_wrong_gives_one():
    assert error_rate(np.array([1, 0]), np.array([0, 1])) == 1.0


def test_3_half_wrong_gives_one_half():
    assert abs(error_rate(np.array([0, 0]), np.array([0, 1])) - 0.5) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(error_rate(np.array([1]), np.array([1])), float)


def test_5_error_plus_accuracy_is_one():
    pred = np.array([0, 1, 1, 0])
    y = np.array([0, 1, 0, 0])
    accuracy = float(np.mean(pred == y))
    assert abs(error_rate(pred, y) + accuracy - 1.0) < 1e-12


def test_6_does_not_mutate_inputs():
    pred = np.array([0, 1])
    error_rate(pred, np.array([1, 1]))
    np.testing.assert_array_equal(pred, [0, 1])

